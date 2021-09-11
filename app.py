from flask import Flask, request

app = Flask(__name__)

@app.route('/manage_file/', methods=['GET'])
def manage_file():
    json = request.get_json();
    return "Got the action: " + json['action']
