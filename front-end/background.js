chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.url) {
        chrome.storage.local.set({ currentUrl: changeInfo.url });

        chrome.action.setPopup({
            tabId: tab.id,
            popup: `popup.html?url=${encodeURIComponent(changeInfo.url)}`
        });
    }
});
