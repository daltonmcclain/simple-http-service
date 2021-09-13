from os import error

from flask import Flask, request
from flask_mongoengine import MongoEngine
import mongoengine as me
import pymongo.errors
from requests import get

# Create our Flask application, called "app"
app = Flask(__name__)

# Setup the app to use mongodb
app.config['MONGODB_SETTINGS'] = {
    'db' : 'simple-http-service_database',
    'host' : 'localhost',
    'port' : 27017
}
db = MongoEngine(app)

# Create a simple Document class for the sample file
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
        
        # Try to download the sample file and save it in a mongo database. Send a 503 error if we can't save to the database.
        try:
            download_url(sample_url)
        except pymongo.errors.ServerSelectionTimeoutError:
            app.logger.error("Error: ServerSelectionTimeout")
            return "Error: there was a problem connecting to the database server", 503
        except:
            raise

        return "Success", 200

    elif action == "read":
        #TODO: Return the contents of the test file
        #TODO: Check if we have the file and return the proper error if we don't 

        # Read the file from the mongo database
        return read_file_from_mongo(sample_url)

    # Didn't get a valid action (download or read)
    else:
        app.logger.error("Error: invalid action")
        app.logger.error("action provided: " + action)
        return "Error: invalid action", 400


# Function to download a file from a url and store it in the mongo database
#TODO: Don't create duplicates
def download_url(url):
    response = get(url)
    print(response.encoding)
    print(response.content.decode())
    text_file = TextFile(filename=url.rsplit('/', 1)[-1], source=url, data=response.content.decode())
    text_file.save()

#TODO: Write a function for reading from the database
def read_file_from_mongo(url):
    text_file = TextFile.objects(source=url).first()
    return text_file.data

# This let's us use "python3 app.py" in order to start the service
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
