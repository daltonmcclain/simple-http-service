from os import error
from flask import Flask, request
from requests import get

# Create our Flask application, called "app"
app = Flask(__name__)

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
        raise

    # Check which action we are getting
    if action == "download":
        sample_url = "https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt"
        download_url(sample_url, "sample-text-file.txt")

        #TODO: Store the file in a mongo database?
        #TODO: Error handling for file request
        return 200

    elif action == "read":
        #TODO: Return the contents of the test file

        return "Got the read action"

    # Didn't get a valide action (download or read)
    else:
        app.logger.error("Error: invalid action")
        app.logger.error("action provided: " + action)
        return "Error: invalid action", 400


# Function to download a file from a url and store it locally
def download_url(url, output_file):
    with open(output_file, "wb") as file:
        response = get(url)
        file.write(response.content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)