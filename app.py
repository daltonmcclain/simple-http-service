from os import error

from flask import Flask, request
from flask_mongoengine import MongoEngine
import mongoengine as me
import pymongo.errors
from requests import get
import requests

# Create our Flask application, called "app"
app = Flask(__name__)

# Setup the app to use mongodb
app.config['MONGODB_SETTINGS'] = {
    'db' : 'simple-http-service_database',
    'host' : 'localhost',
    'port' : 27017
}
db = MongoEngine(app)

# Create a simple Document class for reading/writing the sample file to/from the database
class TextFile(me.Document):
    source = me.StringField()
    filename = me.StringField()
    data = me.StringField()


# We only need a GET route for this app, exposed at the /manage_file endpoint
@app.route('/manage_file', methods=['GET'])
def manage_file():
    # Ensure we are getting json with an action in the request body
    try:
        json_response = request.get_json();
        action = json_response['action'];
    except TypeError:
        app.logger.error("Error: no json provided in the request")
        return "Error: no json provided in request", 400
    except KeyError:
        app.logger.error("Error: no action provided in request")
        return "Error: no action provided in request", 400
    except Exception:
        # In case there's an unforeseen error
        raise

    sample_url = "https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt"

    # Check which action we are getting
    if action == "download":
        # Try to download the sample file and save it in a mongo database
        return download_url("https://bad-url")

    elif action == "read":
        # Read the file from the mongo database
        return read_file_from_mongo(sample_url)
        
    # Didn't get a valid action (download or read)
    else:
        app.logger.error("Error: invalid action")
        app.logger.error("action provided: " + action)
        return "Error: invalid action", 400


# Function to download a file from a url and store it in the mongo database
def download_url(url):
    app.logger.info("Getting data from url: " + url)
    # GET data from this URL; 404 if we can't
    try:
        response = get(url)
    except requests.ConnectionError:
        app.logger.error("ConnectionError: coudln't connect to:" + url)
        return "Error: no response from the specified url: " + url, 404

    # Try to save the data to the mongo database; 503 if we can't connect to the mongo database properly
    try:
        text_file = TextFile.objects(filename=url.rsplit('/', 1)[-1], source=url, data=response.content.decode()).first()
        app.logger.info("Adding url data to mongodb")
        if text_file is None:
            app.logger.info("Couldn't find an existing mongodb entry; adding a new one")
            text_file = TextFile(filename=url.rsplit('/', 1)[-1], source=url, data=response.content.decode())
            text_file.save()
        else:
            app.logger.info("Found an existing mongodb entry; updating it")
            text_file.update(filename=url.rsplit('/', 1)[-1], source=url, data=response.content.decode())
        return "Success", 200
    except pymongo.errors.ServerSelectionTimeoutError:
        app.logger.error("Error: ServerSelectionTimeout")
        return "Error: there was a problem connecting to the database server", 503
    
# Function to read an entry from the database matching a url
def read_file_from_mongo(url):
    # Grab the first entry from the database matching the url; should only be one
    # Return 503 if we can't connect to the server
    try:
        text_file = TextFile.objects(source=url).first()
    except pymongo.errors.ServerSelectionTimeoutError:
        app.logger.error("Error: ServerSelectionTimeout")
        return "Error: there was a problem connecting to the database server", 503

    # 404 if there isn't a matching database entry
    if text_file is None:
        app.logger.error("Error: no entry found for url" + url)
        return "Error: no entry found for url: " + url, 404
    return text_file.data

# This let's us use "python3 app.py" in order to start the service
# Can add "debug=true" if we want the server to output info logging and auto-update during development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
