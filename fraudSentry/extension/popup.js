document.getElementById('scanBtn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  document.getElementById('status').innerText = "Scanning...";

  // Send the URL to your Flask server
  const response = await fetch('http://127.0.0.1:5000/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: tab.url })
  });

  const result = await response.json();
  document.getElementById('status').innerText = result.message;
});