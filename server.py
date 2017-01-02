
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, json, request, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def api_hello():
    return 'TP+ Export API'

@app.route('/export', methods = ['POST'])
def api_export():
    if request.headers['Content-Type'] == 'application/json':
        workout = request.get_json();
        data = export_MRC(workout);
        response = make_response(data);
        response.headers["Content-Disposition"] = "attachment; filename=workout.txt"
        return response;
    else:
        data = "{status: false, description: '415 Unsupported Media Type'}";
        return jsonify(data);
    return;


def export_MRC(workout):
    return;
