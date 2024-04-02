chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "logUrl") {
        console.log("URL logged:", message.url);
    }
});


chrome.webRequest.onCompleted.addListener(function(details) {
    if (details.type === "main_frame") {
        chrome.runtime.sendMessage({ action: 'logUrl', url: details.url });
    }
}, { urls: ["<all_urls>"] });
