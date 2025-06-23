chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const tab = tabs[0];
    const tablink = tab.url;
    const urlDisplay = document.getElementById("url-display");
    const progressContainer = document.querySelector(".progress-container");

    urlDisplay.style.display = "none";
    progressContainer.style.display = "block";  

    const data = { url: tablink };

    function startPhishingCheck() {
        fetch('http://127.0.0.1:5000/process', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(res => {
            progressContainer.style.display = "none";
            urlDisplay.style.display = "block";

            if (res && res.prediction && res.prediction.length > 0) {
                const predictionValue = res.prediction[0];
                if (predictionValue === 0) {
                    
                    urlDisplay.innerHTML = "Suspicisous Site🚫!! Go back⬅️!!";
                    urlDisplay.classList.add("result-phishing");
                    chrome.tabs.update(tab.id, { url: chrome.runtime.getURL("warning.html") });
                } else if (predictionValue === 1) {
                    urlDisplay.innerHTML = "Good to go✅";
                    urlDisplay.classList.add("result-safe");
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    startPhishingCheck();
});
