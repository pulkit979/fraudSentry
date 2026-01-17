# FRAUD-SENTRY

#HOW TO USE:

## Backend Setup

To run the backend server locally, follow these steps:

1.  **Install Python Dependencies**
    Open your terminal and run the following command to install Flask and the required AI libraries:
    ```bash
    pip install flask flask-cors google-genai
    ```

2.  **Set up your API Key (Optional)**
    By default, the app looks for a `GEMINI_KEY` environment variable. You can set it in your terminal before running the app:
    * **Windows (cmd):** `set GEMINI_KEY=your_actual_api_key_here`
    * **Mac/Linux:** `export GEMINI_KEY="your_actual_api_key_here"`

3.  **Start the Server**
    Run the Python script to start the Flask backend:
    ```bash
    python app.py
    ```
    *Replace `app.py` with the actual name of your python file if it is different.*

The server will start on `http://127.0.0.1:5000`.

## Extension Setup (Frontend)

To load the "Fraud-Sentry" extension into Google Chrome:

1.  **Open Extensions Management**
    Open Google Chrome and type `chrome://extensions/` in the address bar, then press Enter.

2.  **Enable Developer Mode**
    In the top-right corner of the Extensions page, toggle the switch for **"Developer mode"** to ON.

3.  **Load the Extension**
    * Click the **"Load unpacked"** button that appears in the top-left corner.
    * Navigate to the folder where you downloaded this repository.
    * Select the specific folder containing the `manifest.json` file named `extension`.

4.  **Pin the Extension**
    * Once loaded, look for the "Puzzle Piece" icon in your Chrome toolbar.
    * Find "Fraud-Sentry" in the list and click the "Pin" icon to make it visible.

**Note:** Ensure your Backend Server (`python app.py`) is running before trying to analyze any URLs with the extension.

## Stop Scams Before You Pay.

---

### A second pair of eyes for every online transaction.

---

## THE PROBLEM

Online scams have evolved.

Phishing websites, fake payment links, and fraudulent checkout pages are now so convincing that **even technically aware users** fall victim.

The problem isn’t carelessness.  
The problem is **timing**.

Fraud happens in the few seconds *before* a payment is made — when users have no visibility and no warning.

---

## THE IDEA

### Fraud-Sentry intervenes *before* the damage is done.

Fraud-Sentry is a browser extension and mobile tool that silently inspects payment links and websites **in real time**, acting as a last line of defense before users enter sensitive details.

It does not block.  
It does not confuse.  
It simply **warns**.

---

## WHAT IT CHECKS

Before a user clicks “Pay”, Fraud-Sentry looks for high-risk signals such as:

- Newly created or suspicious domains  
- Look-alike or manipulated URLs  
- SSL certificate inconsistencies  
- Patterns commonly associated with known scams  

These signals are combined into a **clear risk verdict**:

SAFE  
SUSPICIOUS  
DANGEROUS  

No technical noise. Only actionable clarity.

---

## TECH STACK

Built to be fast, minimal, and hackathon-ready.

-**Frontend**: HTML5, CSS3, JavaScript (Chrome Extension Manifest V3)

-**Backend**: Python, Flask, Flask-CORS

-**AI Model**: Google Gemini 2.5 Flash

-**Database**: SQLite3

-**Analytics**: Chart.js, Bootstrap 5  

The goal is **speed and explainability**, not black-box complexity.

---

## USE CASES

Fraud-Sentry protects users when they are:

- Shopping on unfamiliar e-commerce websites  
- Making UPI or card payments  
- Clicking payment links from messages or emails  

The warning appears **before** sensitive data is entered — exactly when it matters most.

---

## WHY THIS MATTERS

Fraud does not exploit technology.  
It exploits **trust**.

Fraud-Sentry restores balance by giving users visibility at the most critical moment — the decision point.

Less panic.  
Fewer mistakes.  
More informed choices.

---

## PROJECT CONTEXT

This project was built as a **hackathon prototype** to demonstrate how simple, transparent security checks can significantly reduce real-world financial fraud.

It is designed to be:

Minimal  
Understandable  
Immediately useful  

---

## FINAL NOTE

### If a payment requires blind trust, it probably deserves a second look.

That second look is Fraud-Sentry.
