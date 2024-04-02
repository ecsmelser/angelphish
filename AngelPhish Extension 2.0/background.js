// console.log('Extension is running!');

chrome.runtime.onStartup.addListener( () => {
    console.log(`onStartup()`);
});


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'logUrl') {
        saveURL(message.url);
    }
});

function saveURL(url) {
    localStorage.setItem('websiteURL', url);
}

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve URL from localStorage
    const websiteURL = localStorage.getItem('websiteURL');

     // Check if URL exists in localStorage
    if (websiteURL) {
        // Update HTML content with the retrieved URL
    console.log('Extension is running!');
    document.getElementById('phishing-url').innerText = 'Phishing URL: ' + websiteURL;
    } else {
        // Handle case where URL is not found in localStorage
        document.getElementById('phishing-url').innerText = 'No phishing URL found.';
    }
});
