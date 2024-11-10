from flask import Flask, render_template_string
import requests
import pandas as pd
import json  # Import the json module

app = Flask(__name__)

# API URL for Meteoblue with your provided API key and coordinates
url = "https://my.meteoblue.com/packages/basic-day?apikey=aVAZbRQNPt81I5rn&lat=41.5667&lon=23.7333&asl=535&format=json"

@app.route('/weather', methods=['GET'])
def get_weather():
    # Make the request to the Meteoblue API
    response = requests.get(url)
    print(json.dumps(data, indent=4))  # Pretty print the response to check its structure

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant weather data
        weather_description = data['daily']['weather'][0]['description']
        temperature = data['daily']['temperature_2m_max'][0]
        humidity = data['daily']['humidity_2m_max'][0]
        
        # Create a Pandas DataFrame to structure the data
        weather_data = pd.DataFrame([{
            'Weather': weather_description,
            'Temperature (°C)': temperature,
            'Humidity (%)': humidity
        }])
        
        # Convert the DataFrame to HTML
        weather_html = weather_data.to_html(index=False, classes='weather-table')
        
        # HTML template for displaying the weather data
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weather Information</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                h1 {{ color: #4CAF50; }}
                .weather-info {{ font-size: 18px; margin-top: 20px; }}
                .weather-table {{ border-collapse: collapse; width: 100%; }}
                .weather-table th, .weather-table td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
                .weather-table th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Weather Information</h1>
            <div class="weather-info">
                <p><strong>Weather:</strong> {weather_description}</p>
                <p><strong>Temperature:</strong> {temperature}°C</p>
                <p><strong>Humidity:</strong> {humidity}%</p>
            </div>
            <h2>Weather Data Table</h2>
            {weather_html}
        </body>
        </html>
        """
        
        # Return the HTML content
        return render_template_string(html_content)
    else:
        # Handle error if the API request fails
        return f"Error: Unable to fetch weather data (status code: {response.status_code})"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
