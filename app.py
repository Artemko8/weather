from flask import Flask, jsonify
import requests
import pandas as pd
import json

app = Flask(__name__)

@app.route('/weather')
def get_weather():
    url = "https://my.meteoblue.com/packages/basic-day?apikey=aVAZbRQNPt81I5rn&lat=41.5667&lon=23.7333&asl=535&format=json"
    
    try:
        # Fetch weather data
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4xx/5xx errors
        data = response.json()  # Parse the JSON response
        
        # Debugging: print out the entire structure of the data
        print(json.dumps(data, indent=4))  # Pretty print the entire JSON response

        # Extract data for table rows
        weather_data = []
        for forecast in data.get('data', []):  # Adjusted to handle the correct data structure
            row = {
                "date": forecast.get('date'),
                "temperature": forecast.get('temperature'),
                "precipitation": forecast.get('precipitation'),
                "windspeed": forecast.get('windspeed'),
                "winddirection": forecast.get('winddirection'),
            }
            weather_data.append(row)

        # Convert the weather data to a Pandas DataFrame
        df = pd.DataFrame(weather_data)

        # Convert the DataFrame to HTML and style it with Bootstrap
        html_table = df.to_html(classes="table table-bordered table-striped", index=False)

        # Return the HTML page with the weather data
        return html_table

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "message": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": "Invalid JSON response", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
