chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'logUrl') {
        sendDataToServer(message.url);
    }
});

function sendDataToServer(url) {
    // Send the URL to the server for analysis
    // You can use AJAX, Fetch API, etc. to send data to your server
}