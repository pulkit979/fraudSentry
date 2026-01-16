from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.genai as genai
import json
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure Gemini AI
API_KEY = os.getenv("GEMINI_KEY", "AIzaSyBKaVM2kxfsYFZvwky1Iv36wVQtLRyYMV8")

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"
# Initialize Database
def init_db():
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            is_scam INTEGER NOT NULL,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Call this when app starts
init_db()

# Save scan results to database
def save_to_db(url, status, score):
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    is_scam = 1 if status != "safe" else 0 
    c.execute("INSERT INTO scans (url, is_scam, score) VALUES (?, ?, ?)", 
              (url, is_scam, score))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "<h1>Fraud-Sentry Backend is Online!</h1><p><a href='/dashboard'>View Dashboard</a></p>"

@app.route('/check', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')
    page_text = data.get('text', '')[:1500]

    prompt = f"""
    You are 'Fraud-Sentry'. Analyze this URL: {url}
    Context text: {page_text}

    Return ONLY a raw JSON object with this exact structure:
    {{
      "status": "safe" | "suspicious" | "dangerous",
      "trust_score": 0-100,
      "reason": "One sentence explanation",
      "action": "What the user should do",
      "highlights": ["list", "of", "scammy", "phrases"]
    }}
    """
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        
        # Parse and validate JSON
        result = json.loads(clean_json)
        
        # Save to database
        save_to_db(url, result.get('status'), result.get('trust_score'))
        
        print(f"\n[SCAN] {url}")
        print(f"STATUS: {result.get('status')} | SCORE: {result.get('trust_score')}/100")
        
        return clean_json, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "reason": "AI Analysis Failed"}), 500

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()
    
    # Get total counts for summary cards
    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scans WHERE is_scam = 1")
    scams_found = cursor.fetchone()[0]
    
    # Get data for the Chart (Safe vs Scam)
    cursor.execute("SELECT is_scam, COUNT(*) FROM scans GROUP BY is_scam")
    chart_data = cursor.fetchall()
    
    # Get last 10 scans for the table
    cursor.execute("SELECT url, is_scam, score, timestamp FROM scans ORDER BY timestamp DESC LIMIT 10")
    recent_scans = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                           total=total_scans, 
                           scams=scams_found, 
                           recent=recent_scans)

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)