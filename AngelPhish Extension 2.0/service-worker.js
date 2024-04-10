console.log('Extension is running!');

chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs) {
    var url = tabs[0].url;
    console.log("Most recent URL: " + url);
});
