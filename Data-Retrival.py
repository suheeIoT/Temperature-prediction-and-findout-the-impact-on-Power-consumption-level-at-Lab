import influxdb_client    # Client Library for InfluxDB  
from influxdb_client.client.write_api import SYNCHRONOUS  # Write API library for Sync 
import csv   # importing csv library
bucket = "Lab-Temperature"  # Bucket name of InfluxDB
org = "NokiaFrance"   # Organization name of InfluxDB
token = ""    # Token for Lab-Temperature bucket at influxDB. This token contains Read & Write permission

# Store the URL of your InfluxDB instance
url=""    # URL for an InfluxDB – This is an IP address of the Laptop (InfluxDB)
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)   # Created an object called Client which contains URL, Token, and Org
# Query script uses to retrieve the data for 10 years from InfluxDB ( Flux Language)

query_api = client.query_api()   # Defined a variable and named query_api
query = 'from(bucket:"Lab-Temperature")\          # From location – Bucket name 
|> range(start: 2023-05-20T00:00:00Z, stop: 2033-05-23T00:00:00Z)\       # Duration for a retrieval 
|> filter(fn:(r) => r._measurement == "Data")\      # Measurement name at InfluxDB
|> filter(fn:(r) => r.location == "Nokia")\                # Location name at InfluxDB
|> filter(fn:(r) => r._field == "LAB_Temperature")   # Field for Retrieval – Only Temp data
|> timeShift(duration: 2h)' # Uses to convert time format from UTC to CEST --> UTC+2 in flux language

#|> filter(fn:(r) => r._field == "LAB_Temperature" or r._field == "LAB_Humidity")'



result = query_api.query(org=org, query=query)          # Create a variable called Result and save a query data
results = []      #  retrieve all the data in array

for table in result:
    for record in table.records:
          results.append((record.get_time(),record.get_value()))  # Retrieving time & Temperature Value and store into the same result array

print("Temperature values are :",results)    # Printing values for Temperature data

with open(r'C:\Nokia_Project\Temperatures_DB.csv', 'w', newline='') as file:      # This will create a Temperature.csv file under the path where, the Python script is running (Pull data from InpluxDB.py )
     writer = csv.writer(file)    # This method used to create a writer object from imported CSV library
     writer.writerows(results)   # This method uses to write all the data in the list
     print("Temperatures_DB.CSV file is successfully created !")   # Display message 




