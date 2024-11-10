from flask import Flask, jsonify
import requests
import json  # Import the json module

app = Flask(__name__)

@app.route('/weather')
def get_weather():
    url = "https://my.meteoblue.com/packages/basic-day?apikey=aVAZbRQNPt81I5rn&lat=41.5667&lon=23.7333&asl=535&format=json"
    
    # Attempt to get data from the API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
        
        # Try to parse the JSON response
        data = response.json()

        # Pretty print the response (only for debugging)
        print(json.dumps(data, indent=4))  # Now json is imported, this will work

        # Return the data as JSON response
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        # Handle HTTP or network errors
        return jsonify({"error": "Request failed", "message": str(e)}), 500

    except ValueError as e:
        # Handle invalid JSON response
        return jsonify({"error": "Invalid JSON response", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
