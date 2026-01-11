from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ADD THIS PART: The Home Route
@app.route('/')
def home():
    return "<h1>Fraud-Sentry Server is LIVE!</h1><p>The backend is waiting for requests from the extension.</p>"

# This is your existing route for the extension
@app.route('/check', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')
    print(f"Checking URL: {url}")
    return jsonify({"message": f"Verified: {url}", "status": "safe"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)