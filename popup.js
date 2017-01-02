function go() {

	if (document.getElementById('MRC').checked) {
		var fileFormat = document.getElementById('MRC').value;
		var FTP = null;
	} else if (document.getElementById('ERG').checked) {
		var fileFormat = document.getElementById('ERG').value;
		var FTP = document.getElementById('FTP').value;
	} else if (document.getElementById('ZWO').checked) {
		var fileFormat = document.getElementById('ZWO').value;
		var FTP = null;
	} else {
		var fileFormat = null;
		var FTP = null;
	}

	chrome.tabs.executeScript(null, {
		//code: "var fileFormat = '" + fileFormat + "';"
		code: "var fileFormat = '" + fileFormat + "';\nvar FTP=" + FTP + ";"
	}, function () {
		chrome.tabs.executeScript(null, {
			file: 'content-script.js'
		});
	});
}

document.getElementById('export').addEventListener('click', go);