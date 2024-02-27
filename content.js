chrome.webRequest.onCompleted.addListener(function(details) {
    if (details.type === "main_frame") {
        chrome.runtime.sendMessage({ action: 'logUrl', url: details.url });
    }
}, { urls: ["<all_urls>"] });