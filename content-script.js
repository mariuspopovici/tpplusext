

if (fileFormat == 'undefined' || fileFormat == null) {
	var fileFormat = "MRC";
}

if (FTP == 'undefined' || FTP == null) {
	var FTP = 300;
}

var groupsElements = $(".stepList");

if (groupsElements.length == 0) {
	jAlert("Can't find any exportable workouts on current page!", 'TP+ Export Warning');
} else {
	exportWorkout();
}

function exportWorkout() {

	var sWorkoutTitle = $(".workoutTitle").val();
	if (!sWorkoutTitle) {
		sWorkoutTitle = "Untitled workout";
	}
	var re = /(\d+\sx\s)?\d+\s(min|sec)\s@\s\d+\sW/igm;
	var workout = {
		name: sWorkoutTitle,
		description: "",
		groups: [],
		FTP: FTP
	}

	for (var i = 0; i < groupsElements.length; i++) {
		var groupElement = groupsElements[i];
		var groupString = groupElement.innerText;
		var stepArray = groupString.match(re);

		var group = {
			description: groupString,
			repeat: 1,
			steps: []
		}

		if (stepArray) {
			for (var j = 0; j < stepArray.length; j++) {
				var stepString = stepArray[j];
				var stepInfo = stepString.split(' ');
				var nOffset = 0;
				if (stepInfo[1] === 'x') {
					// remove the multiplier in step description
					stepString = stepString.substr(stepString.indexOf('x') + 2, stepString.length);
					// skip the multiplier in stepInfo
					nOffset = 2;
					group.repeat = parseInt(stepInfo[0]);
				}
				var step = {
					description: stepString,
					duration: parseInt(stepInfo[0 + nOffset]),
					timeUnits: stepInfo[1 + nOffset],
					intensity: parseInt(stepInfo[3 + nOffset]),
					intensityRef: 'FTP'
				}
				group.steps.push(step);
			}
		}

		workout.groups.push(group);
	}

	postWorkout(workout, fileFormat);
}

function postWorkout(workout, fileFormat) {
	$.ajax({
		type: "POST",
		//the url where you want to sent the userName and password to
		url: 'https://mariusp.pythonanywhere.com/export',
		dataType: 'json',
		contentType: "application/json",
		async: true,
		crossdomain: true,
		data: JSON.stringify({
			Workout: workout,
			Format: fileFormat
		}),
		success: function (data) {
			if (data.status) {
				var blob = new Blob([data.content], {
					type: "text/plain;charset=utf-8"
				});
				saveAs(blob, workout.name + "." + fileFormat.toLowerCase());
			} else {
				jAlert('TP+ Error: error calling remote API.', 'TP+ Export Error');
			}
		},
		error: function (xhr, textStatus, errorMessage) {
			jAlert(errorMessage, 'TP+ Export Error');
		}
	});
}

function saveFile(data, fileName) {

}
