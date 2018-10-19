function go() {

  var fileFormat = null, FTP = null;


	if (document.getElementById('MRC').checked) {
		fileFormat = document.getElementById('MRC').value;
		FTP = document.getElementById('FTP').value;
	} else if (document.getElementById('ERG').checked) {
		fileFormat = document.getElementById('ERG').value;
		FTP = document.getElementById('FTP').value;
	} else if (document.getElementById('ZWO').checked) {
		fileFormat = document.getElementById('ZWO').value;
		FTP = null;
	}

	chrome.tabs.executeScript(null, {
		code: "var fileFormat = '" + fileFormat + "';\nvar FTP=" + FTP + ";"
	}, function () {
		chrome.tabs.executeScript(null, {
			file: 'content-script.js'
		});
	});
}

document.getElementById('export').addEventListener('click', go);

var _AnalyticsCode = 'UA-89710256-1';

var _gaq = _gaq || [];
_gaq.push(['_setAccount', _AnalyticsCode]);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script');
  ga.type = 'text/javascript';
  ga.async = true;
  ga.src = 'https://ssl.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(ga, s);
})();
