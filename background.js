function checkForValidUrl(tabId, changeInfo, tab) {
	if (tab.url.indexOf('http://app.trainingpeaks.com') == 0 ||
		tab.url.indexOf('https://app.trainingpeaks.com') == 0) {
		chrome.pageAction.show(tabId);
	}
};

chrome.tabs.onUpdated.addListener(checkForValidUrl);
