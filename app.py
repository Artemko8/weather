from flask import Flask, render_template
import requests
import pandas as pd  # Import pandas
import json

app = Flask(__name__)

@app.route('/weather')
def get_weather():
    url = "https://my.meteoblue.com/packages/basic-day?apikey=aVAZbRQNPt81I5rn&lat=41.5667&lon=23.7333&asl=535&format=json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
        
        # Parse the JSON response
        data = response.json()

        # Convert the JSON data into a Pandas DataFrame
        df = pd.json_normalize(data)  # Flatten the JSON data into a table format

        # Render the DataFrame as an HTML table
        html_table = df.to_html(classes="table table-bordered table-striped", index=False)

        # Return the HTML page with the weather data
        return render_template('weather.html', table=html_table)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "message": str(e)}), 500

    except ValueError as e:
        return jsonify({"error": "Invalid JSON response", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
