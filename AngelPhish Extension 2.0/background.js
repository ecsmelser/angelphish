chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'logUrl') {
        saveURL(message.url);
    }
});

function saveURL(url) {
    localStorage.setItem('websiteURL', 'https://example.com')
}

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve URL from localStorage
    const websiteURL = localStorage.getItem('websiteURL=');

    // Check if URL exists in localStorage
    if (websiteURL) {
        // Update HTML content with the retrieved URL
        document.getElementById('phishing-url').innerText = 'Phishing URL: ' + websiteURL;
    } else {
        // Handle case where URL is not found in localStorage
        document.getElementById('phishing-url').innerText = 'No phishing URL found.';
    }
});