// This runs as soon as you click the extension icon and the popup opens
document.addEventListener('DOMContentLoaded', () => {
    // 1. Check if there is data from a recent scan
    chrome.storage.local.get('lastScan', (data) => {
        if (data.lastScan) {
            const res = data.lastScan;
            const fill = document.getElementById('meter-fill');
            const scoreText = document.getElementById('score-text');
            const details = document.getElementById('details');

            // 2. Update the visual Trust Meter
            fill.style.width = res.trust_score + "%";
            
            // Color logic: Red (0-39), Orange (40-69), Green (70-100)
            if (res.trust_score < 40) {
                fill.style.background = "#e74c3c"; // Dangerous Red
            } else if (res.trust_score < 70) {
                fill.style.background = "#f39c12"; // Suspicious Orange
            } else {
                fill.style.background = "#2ecc71"; // Safe Green
            }
            
            // 3. Update the Text
            scoreText.innerText = `Trust Score: ${res.trust_score}%`;
            details.innerHTML = `
                <div style="margin-top:10px; border-top:1px solid #ddd; padding-top:10px;">
                    <strong>Status:</strong> <span style="color:${fill.style.background}">${res.status.toUpperCase()}</span><br>
                    <p style="font-size:12px; color:#666;">${res.reason}</p>
                    <p style="font-size:11px; font-weight:bold;">Recommendation: ${res.action}</p>
                </div>
            `;
        } else {
            document.getElementById('details').innerText = "Visit a website to see the AI scan results.";
        }
    });
});