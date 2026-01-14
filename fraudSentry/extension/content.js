(function() {
    // Only send text if the page is not empty
    const pageText = document.body.innerText.substring(0, 1500);
    const currentUrl = window.location.href;

    // Use localhost instead of 127.0.0.1 for better browser compatibility
    fetch('http://localhost:5000/check', {
        method: 'POST',
        mode: 'cors', // Explicitly set CORS mode
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: currentUrl, text: pageText })
    })
    .then(res => {
        if (!res.ok) throw new Error('Network response was not ok');
        return res.json();
    })
    .then(data => {
        chrome.storage.local.set({ lastScan: data });

        if (data.status !== 'safe') {
            injectWarningBanner(data);
            highlightScams(data.highlights);
        }
    })
    .catch(err => console.log("Fraud-Sentry: Server is not reachable. Is app.py running?"));

    function injectWarningBanner(data) {
        if (document.getElementById('fraud-sentry-banner')) return;
        const div = document.createElement('div');
        div.id = 'fraud-sentry-banner';
        div.style.cssText = `position:fixed;top:0;left:0;width:100%;z-index:2147483647;
                            background:${data.status === 'dangerous' ? '#cc0000' : '#f39c12'};
                            color:white;padding:15px;text-align:center;font-weight:bold;
                            box-shadow: 0 2px 10px rgba(0,0,0,0.5); font-family: sans-serif;`;
        div.innerHTML = `🛡️ Fraud-Sentry: ${data.reason} <button id="close-sentry" style="margin-left:20px; cursor:pointer;">Ignore</button>`;
        document.body.prepend(div);
        document.getElementById('close-sentry').onclick = () => div.remove();
    }

    function highlightScams(phrases) {
        if (!phrases || phrases.length === 0) return;
        phrases.forEach(p => {
            if (p.length < 4) return; // Avoid highlighting single letters
            const safePhrase = p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            document.body.innerHTML = document.body.innerHTML.replace(
                new RegExp(safePhrase, 'gi'),
                match => `<mark style="background:red;color:white;padding:2px;border-radius:3px;">🚩 ${match}</mark>`
            );
        });
    }
})();