document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scanBtn');
    const resultDisplay = document.getElementById('result-display');
    const progressCircle = document.getElementById('progress-circle');
    const scoreText = document.getElementById('score-text');
    const statusValue = document.getElementById('status-value');
    const reasonText = document.getElementById('reason-text');

    // Load last scan from storage
    chrome.storage.local.get('lastScan', (data) => {
        if (data.lastScan) {
            updateUI(data.lastScan);
        }
    });

    scanBtn.addEventListener('click', async () => {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        statusValue.innerText = "ANALYZING...";
        resultDisplay.style.display = "flex";

        // 1. Get Text from Content Script
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => document.body.innerText.substring(0, 1500)
        }, async (results) => {
            const pageText = results[0].result;

            // 2. Fetch from Localhost Backend
            try {
                const response = await fetch('http://localhost:5000/check', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: tab.url, text: pageText })
                });

                const data = await response.json();
                
                // 3. Save and Update UI
                chrome.storage.local.set({ lastScan: data });
                updateUI(data);

                // 4. Send signal back to page to show banner/highlights
                chrome.tabs.sendMessage(tab.id, { action: "applyUI", data: data });

            } catch (error) {
                statusValue.innerText = "OFFLINE";
                reasonText.innerText = "Make sure app.py is running.";
            }
        });
    });

    scanBtn.addEventListener('click', async () => {
    // 1. Start the animation & change text
    scanBtn.classList.add('is-scanning');
    const buttonText = scanBtn.querySelector('.div');
    const originalText = buttonText.innerText;
    buttonText.innerText = "SCANNING...";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // 2. Send message to content.js (from your current code)
    chrome.tabs.sendMessage(tab.id, { action: "manualScan" }, (response) => {
        
        // 3. Stop the animation
        scanBtn.classList.remove('is-scanning');
        buttonText.innerText = originalText;

        if (chrome.runtime.lastError || !response) {
            console.error("Scan failed");
            return;
        }

        // 4. Update your Trust Meter UI with the result
        updateUI(response);
    });
});

    function updateUI(res) {
        resultDisplay.style.display = "flex";
        const score = res.trust_score || 0;
        const status = res.status || "suspicious";

        // Update Text
        scoreText.innerText = `${score}%`;
        statusValue.innerText = status.toUpperCase();
        reasonText.innerText = res.reason;

        // Color Logic
        let color = "#2ecc71"; // Safe Green
        if (status === "dangerous") color = "#e74c3c"; // Red
        else if (status === "suspicious") color = "#f39c12"; // Orange

        statusValue.style.color = color;
        scoreText.style.color = color;

        // Animate Circle (conic-gradient)
        const degrees = score * 3.6;
        progressCircle.style.background = `conic-gradient(${color} ${degrees}deg, #333 0deg)`;
    }
});