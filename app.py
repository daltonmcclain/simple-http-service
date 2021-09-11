from os import error
from flask import Flask, request

# Create our Flask application, called "app"
app = Flask(__name__)

# We only need a GET route for this app, exposed at the /manage_file endpoint
@app.route('/manage_file/', methods=['GET'])
def manage_file():
    # Ensure we are getting json with an action in the request body
    try:
        json_response = request.get_json();
        action = json_response['action'];
    except TypeError:
        return "Error: no json provided in request"
    except KeyError:
        return "Error: no action provided in request"
    except Exception:
        raise

    # Check that we are getting an action
    if action == "download":
        return "Got the download action"
        #TODO: Fetch the file at https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt and store it locally

    elif action == "read":
        return "Got the read action"
        #TODO: Return the contents of the test file

    else:
        return "Error: invalid action"



