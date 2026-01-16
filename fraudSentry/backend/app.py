from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)

# FIXED: Corrected model name to gemini-1.5-flash
genai.configure(api_key="AIzaSyBb91txbUqghbrhtMZPKH0u6aS1yLjlc5w") 
model = genai.GenerativeModel('gemini-2.5-flash')

# FIXED: Added Home Route to prevent 404
@app.route('/')
def home():
    return "<h1>Fraud-Sentry Backend is Online!</h1>"

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
        response = model.generate_content(prompt)
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        
        # Test valid JSON
        result = json.loads(clean_json)
        
        print(f"\n[SCAN] {url}")
        print(f"STATUS: {result.get('status')} | SCORE: {result.get('trust_score')}/100")
        
        return clean_json, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "reason": "AI Analysis Failed"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)

import sqlite3
from flask import render_template

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
    chart_data = cursor.fetchall() # Returns something like [(0, 10), (1, 5)]
    
    # Get last 10 scans for the table
    cursor.execute("SELECT url, score, timestamp FROM scans ORDER BY timestamp DESC LIMIT 10")
    recent_scans = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                           total=total_scans, 
                           scams=scams_found, 
                           chart_data=chart_data,
                           table_data=recent_scans)

def save_to_db(url, status, score):
    conn = sqlite3.connect('stats.db')
    c = conn.cursor()
    # 1 for scam, 0 for safe
    is_scam = 1 if status != "safe" else 0 
    c.execute("INSERT INTO scans (url, is_scam, score) VALUES (?, ?, ?)", 
              (url, is_scam, score))
    conn.commit()
    conn.close() 
