import requests
import json
from influxdb_client import InfluxDBClient, WriteOptions

API_key = ''
latitude = 47.564751
longitude = -1.626916

# Replace 'http://proxy_server:port' with your actual proxy server and port if needed
proxies = {
    'http': 'http://135.245.192.7:8000',
    'https': 'http://135.245.192.7:8000',
}

# Configure InfluxDB connection variables
influxdb_url = ""
influxdb_token = ""
org = "NokiaFrance"
bucket = "Lab-Temperature"

try:
     # Create the InfluxDB client
    _client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=org, debug=True)
    _write_client = _client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))

    # Configure the labels for the database
    measurement = "Data"  # Change accordingly
    location = "Nokia"              # Change accordingly

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_key}&units=metric'

    r = requests.get(url, proxies=proxies)
    r.raise_for_status()  # Check for any request errors

    data = r.json()

    # Extract temperature in Celsius from the response
    temperature_celsius = data["main"]["temp"]

    print("Temperature in Celsius:", temperature_celsius, "°C")

            # Push the Temperature and Humidity data into InfluxDB
    _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location},"fields": {"Outdoor_Temperature": temperature_celsius}}])
    
    print("The Temperature data are injected into InfluxDB Successfully!")
except requests.exceptions.RequestException as e:
    print("Error connecting to the API:", e)

_write_client.__del__()
_client.__del__()


