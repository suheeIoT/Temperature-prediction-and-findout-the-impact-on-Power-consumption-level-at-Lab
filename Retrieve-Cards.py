import requests
import json
import base64
import pandas as pd
import datetime
import csv
from influxdb_client import InfluxDBClient, WriteOptions

# Function to get authentication token
def get_token(server_ip, port, server_username, server_password):
    url = f"https://{server_ip}:{port}/rest-gateway/rest/api/v1/auth/token"
    payload = json.dumps({"grant_type": "client_credentials"})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + base64.b64encode((server_username + ":" + server_password).encode('utf-8')).decode('utf-8')
    }
    response = requests.post(url, data=payload, headers=headers, verify=False)
    print("Token Response Content:", response.text)
    data = response.json()
    if response.status_code == 200:
        token = data["access_token"]
        return token
    else:
        raise Exception(f"Unable to get token: {response}")

# Replace these variables with your server details and credentials
server_ip = '135.238.196.72'
port = 8443
server_username = 'Stage'
server_password = 'Nokia@23'

# Get the authentication token
auth_token = get_token(server_ip, port, server_username, server_password)

print('Token is generated successfully!!')

# Replace 'http://proxy_server:port' with your actual proxy server and port if needed
proxies = {
    'http': 'http://135.245.192.7:8000',
    'https': 'http://135.245.192.7:8000',
}

# Configure InfluxDB connection variables
influxdb_url = "http://135.238.196.149:8086"
influxdb_token = "CuX6sTwp063CDQRjXOeerLcdbaGoeS7nt2Pi49nNkDde27BbbDYYZZU1jorna8er1guBYVuOG6fKYKBtHaAXFw=="
influxdb_org = "NokiaFrance"
influxdb_bucket = "Network-Element"

try:
    # Create the InfluxDB client
    _client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org, debug=True)
    _write_client = _client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))

    # Configure the labels for the database
    measurement = "NetworkCards"  # Change accordingly
    location = "Nokiaa"              # Change accordingly

    # API endpoint
    api_endpoint = "/npr-process/emlnemgr/NE/RIReport/"

    # Construct the URL using the IP address and port
    url = f"https://{server_ip}:{port}{api_endpoint}"

    # Make the request using the proxies parameter and the authentication token in headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    data = {
        "neList": "ALL",
        "packType": "ALL"
    }

    response_API = requests.post(url, json=data, headers=headers, proxies=proxies, verify=False)

    # Check if the API call was successful
    if response_API.status_code == 200:
        data = response_API.json()
     
        # Prepare the CSV file
        csv_filename = r'C:\Nokia_Project\Temperature\Card_details.csv'
        with open(csv_filename, mode="a", newline="") as csv_file:  # mode 'a' uses to append data into csv file
            fieldnames = ["Date", "Terminal_ID","Card_ID", "Card_Temperature", "Card_Power"]
            dict_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)  # Creating dictionary
            print("Card Details for an entire Network elements")
            print("************************************************")
            for item in data:
                tid = item['NE']
                CID = item['id']
                temperature = item['temperature']
                power = item['CardPower']

                if temperature != '0C' and power != '0C' and power != 'N/A' and temperature != 'N/A':  # filter the real values 
                    print("Terminal ID:", tid, ",", "Card ID:", CID, ",", "Card_Temperature:", temperature, ",", "Card_Power:", power)

                    # Get current date and time
                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Write data to InfluxDB
                    _write_client.write(bucket=influxdb_bucket, org=influxdb_org, record=[
                        {"measurement": measurement, "tags": {"location": location, "Terminal ID": tid,"Card ID": CID},
                         "fields": {"Card_Temperature": temperature,"Card_Power": power}}
                    ])

                    dict_writer.writerow({"Date": current_datetime, "Terminal_ID": tid, "Card_ID": CID, "Card_Temperature": temperature,
                                          "Card_Power": power})

        # Close the CSV file outside of the loop
        csv_file.close()

        print("Total no of data written into InfluxDB:", len(data))
        print("The Data are injected into InfluxDB Successfully!")

    else:
        # If the API call was not successful, print an error message
        print("Failed to retrieve data. Status code:", response_API.status_code)

except requests.exceptions.RequestException as e:
    print("Error connecting to the API:", e)
finally:
    if '_write_client' in locals():
        _write_client.__del__()
    if '_client' in locals():
        _client.__del__()
