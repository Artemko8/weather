from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/weather')
def get_weather():
    url = "https://my.meteoblue.com/packages/basic-day?apikey=aVAZbRQNPt81I5rn&lat=41.5667&lon=23.7333&asl=535&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Error fetching data from Meteoblue", 500

    data = response.json()
    
    # Check if data contains 'data_day' and if the required data exists
    if 'data_day' not in data:
        return "Weather data not found", 500

    # Extract data_day values for rendering
    forecast_data = data['data_day']

    # Prepare data for rendering in a table
    rows = []
    for i in range(len(forecast_data['time'])):
        row = {}
        for key in forecast_data:
            row[key] = forecast_data[key][i]  # Dynamically fetch each key's value for the given index
        rows.append(row)

    # Create a DataFrame to easily generate HTML table
    df = pd.DataFrame(rows)

    # Render the HTML table
    html_table = df.to_html(classes='table table-bordered table-striped', index=False)

    return render_template('weather.html', table=html_table)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
