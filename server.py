from __future__ import division
from flask import Flask, json, request, jsonify


app = Flask(__name__)

@app.route('/')
def api_hello():
    return 'TP+ Export API'

@app.route('/export', methods = ['POST'])
def api_export():
    if request.headers['Content-Type'] == 'application/json':
        workout = request.get_json();
        data = export(workout);
        if not (data is None):
            return jsonify(status = True, content = data);
        else:
            return jsonify(status = False, content = None);
    else:
        return jsonify(status = False, content = "415 Unsupported Media Type");
    return;

def export(workout):
    format = workout['Format'];
    workout = workout['Workout'];
    if (format == "MRC"):
        return export_MRC(workout);
    else:
        if (format == "ERG"):
            return export_ERG(workout);
        else:
            return "";

def export_MRC(workout):
    content = ("[COURSE HEADER]\r\nVERSION = 2\r\nUNITS = ENGLISH\r\n"
        "DESCRIPTION = $DESCRIPTION$\r\n"
        "FILE NAME = $FILENAME$\r\n"
        "MINUTES PERCENT\r\n[END COURSE HEADER]\r\n[COURSE DATA]\r\n");

    content = content.replace("$DESCRIPTION$", workout['name']);
    content = content.replace("$FILENAME$", workout['name'] + '.MRC');

    stepTime = 0;
    for group in workout['groups']:
        for repeat in range(0, group['repeat']):
            for step in group['steps']:
                content += str(stepTime) + "\t" + str(step['intensity']) + "\r\n";
                duration = step['duration'];
                if (step['timeUnits'] == "sec"):
                    duration = step['duration'] * 1/60;
                    duration = round(duration, 2);
                stepTime = stepTime + duration;
                content += str(stepTime) + "\t" + str(step['intensity']) + "\r\n";

    content += "[END COURSE DATA]";

    return content;

def export_ERG(workout):
    content = ("[COURSE HEADER]\nVERSION = 2\nUNITS = ENGLISH\n"
        "DESCRIPTION = $DESCRIPTION$\n"
        "FILE NAME = $FILENAME$\nFTP=$FTP$\n"
        "MINUTES WATTS\n[END COURSE HEADER]\n[COURSE DATA]\n");

    content = content.replace("$DESCRIPTION$", workout['name']);
    content = content.replace("$FILENAME$", workout['name'] + '.ERG');
    content = content.replace("$FTP$", str(workout['FTP']));

    stepTime = 0;
    for group in workout['groups']:
        for repeat in range(0, group['repeat']):
            for step in group['steps']:
                wattage = int((step['intensity'] * workout['FTP']) / 100);
                content += str(stepTime) + "\t" + str(wattage) + "\n";
                duration = step['duration'];
                if (step['timeUnits'] == "sec"):
                    duration = step['duration'] * 1/60;
                    duration = round(duration, 2);
                stepTime = stepTime + duration;
                content += str(stepTime) + "\t" + str(wattage) + "\n";

    content += "[END COURSE DATA]";

    return content;
