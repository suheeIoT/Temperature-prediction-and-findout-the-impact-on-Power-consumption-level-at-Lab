import Adafruit_DHT as dht
from time import sleep
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from gpiozero import OutputDevice   # For triggering external cooling system


# Configure InfluxDB connection variables
token = ""
org = "NokiaFrance"
bucket = "Lab-Temperature"

_client = InfluxDBClient(url="", token=token, debug=True)
_write_client = _client.write_api(write_options=WriteOptions(batch_size=500,
                                                             flush_interval=10_000,
                                                             jitter_interval=2_000,
                                                             retry_interval=5_000,
                                                             max_retries=5,
                                                             max_retry_delay=30_000,
                                                             exponential_base=2))


# Configure the labels for the database
measurement = "Data"
location = "Nokia"

# Set DATA pin
DHT = 4  # Defining input pins for three sensors
DHT_A = 6
DHT_B = 12
GPIO_PIN = 17  # Defining output pin
Threshold = 30 # Defining threshold value

fan = OutputDevice(GPIO_PIN) # Assigning output pin
try:
    while True:
        # Read Temp and Hum from DHT22
        Humidity, Temperature = dht.read_retry(dht.DHT22, DHT)
        Humidity_A, Temperature_A = dht.read_retry(dht.DHT22, DHT_A)
        Humidity_B, Temperature_B = dht.read_retry(dht.DHT22, DHT_B)

        if Temperature is not None and Humidity is not None:
            print('Temperature={0:0.1f}*C  Humidity={1:0.1f}%'.format(Temperature, Humidity))
            if Temperature >= Threshold:
                fan.on()  # used to set the GPIO High
                print('External cooling system is activated at centre Zone!')
        elif Temperature_A is None and Humidity_A is not None:
            print('Temperature at zone A ={0:0.1f}*C  Humidity at zone A ={1:0.1f}%'.format(Temperature_A, Humidity_A))
            if Temperature_A >= Threshold:
                fan.on()  # used to set the GPIO High
                print('External cooling system is activated at Zone A!')
        elif Temperature_B is None and Humidity_B is not None:
            print('Temperature at zone B ={0:0.1f}*C  Humidity at zone B ={1:0.1f}%'.format(Temperature_B, Humidity_B))
            if Temperature_B >= Threshold:
                fan.on()  # used to set the GPIO High
                print('External cooling system is activated at Zone B!')

        # Push the Temperature and Humidity data into InfluxDB
        _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location}, # Temperature and Humidity at centre zone
                                           "fields": {"LAB_Temperature": Temperature}}])
        _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location},
                                           "fields": {"LAB_Humidity": Humidity}}])
        sleep(1)
        _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location}, # At zone A
                                           "fields": {"Zone-A": Temperature_A}}])
        sleep(1)
        _write_client.write(bucket, org, [{"measurement": measurement, "tags": {"location": location}, # At zone B
                                           "fields": {"Zone-B": Temperature_B}}])

        print("The Data are injected into InfluxDB Successfully!")

        sleep(5)  # Wait for 5 seconds and read it again
except KeyboardInterrupt:
    pass

_write_client.__del__()
_client.__del__()








