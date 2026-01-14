from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)

# FIXED: Corrected model name to gemini-1.5-flash
genai.configure(api_key="YOUR_API_KEY") 
model = genai.GenerativeModel('gemini-1.5-flash')

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
