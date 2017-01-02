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
    content = ("[COURSE HEADER]\nVERSION = 2\nUNITS = ENGLISH\n"
        "DESCRIPTION = $DESCRIPTION$\n"
        "FILE NAME = $FILENAME$\n"
        "MINUTES PERCENT\n[END COURSE HEADER]\n[COURSE DATA]\n");

    content = content.replace("$DESCRIPTION$", workout['name']);
    content = content.replace("$FILENAME$", workout['name'] + '.MRC');

    for group in workout['groups']:
        for repeat in range(0, group['repeat']):
            for step in group['steps']:
                duration = step['duration'];
                if (step['timeUnits'] == "sec"):
                    duration = step['duration'] * 1/60;
                    duration = round(duration, 2);
                content += str(duration) + " " + str(step['intensity']) + "\n";

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

    for group in workout['groups']:
        for repeat in range(0, group['repeat']):
            for step in group['steps']:
                duration = step['duration'];
                if (step['timeUnits'] == "sec"):
                    duration = step['duration'] * 1/60;
                    duration = round(duration, 2);
                wattage = int((step['intensity'] * workout['FTP']) / 100);
                content += str(duration) + " " + str(wattage) + "\n";

    content += "[END COURSE DATA]";

    return content;

