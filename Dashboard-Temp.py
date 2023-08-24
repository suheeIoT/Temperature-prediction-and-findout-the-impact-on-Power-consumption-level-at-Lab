import influxdb_client
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time
from datetime import datetime

bucket = "Lab-Temperature"
org = "NokiaFrance"
token = ""
url = ""

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api_center = client.query_api()
query_center = '''
from(bucket:"Lab-Temperature")
|> range(start: 2023-05-20T00:00:00Z, stop: 2033-05-23T00:00:00Z)
|> filter(fn:(r) => r._measurement == "Data")
|> filter(fn:(r) => r.location == "Nokia")
|> filter(fn:(r) => r._field == "Temperature at centre zone")
|> timeShift(duration: 2h)
|> last()
'''

query_api_A = client.query_api()
query_A = '''
from(bucket:"Lab-Temperature")
|> range(start: 2023-05-20T00:00:00Z, stop: 2033-05-23T00:00:00Z)
|> filter(fn:(r) => r._measurement == "Data")
|> filter(fn:(r) => r.location == "Nokia")
|> filter(fn:(r) => r._field == "Temperature at Zone-A")
|> timeShift(duration: 2h)
|> last()
'''

query_api_B = client.query_api()
query_B = '''
from(bucket:"Lab-Temperature")
|> range(start: 2023-05-20T00:00:00Z, stop: 2033-05-23T00:00:00Z)
|> filter(fn:(r) => r._measurement == "Data")
|> filter(fn:(r) => r.location == "Nokia")
|> filter(fn:(r) => r._field == "Temperature at Zone-B")
|> timeShift(duration: 2h)
|> last()
'''

# Create initial figure and heatmap
fig, ax = plt.subplots()

heatmap = ax.imshow(np.zeros((1, 3)), cmap='jet', interpolation='nearest', aspect='auto', vmin=22, vmax=38)
plt.colorbar(heatmap, ax=ax)
ax.set_xticks(np.arange(3))
ax.set_xticklabels(["Zone A", "Center Zone", "Zone B"])
ax.set_title("Temperature Dashboard - NokiaLab")

def update_heatmap(frame):
    
    result_A = query_api_A.query(org=org, query=query_A)
    result_center = query_api_center.query(org=org, query=query_center)
    result_B = query_api_B.query(org=org, query=query_B)
    
    temperature_values = []
    for table in [result_A, result_center, result_B]:
        temperature = table[0].records[0].get_value() 
        temperature_values.append(temperature)
    
    heatmap.set_array(np.array(temperature_values).reshape(1, 3))

    # Clear existing annotations
    for annotation in ax.texts:
        annotation.remove()

    # Annotate heatmap cells with temperature values
    for i in range(1):
        for j in range(3):
             text = ax.text(j, i, f"{temperature_values[j]:.1f}°C",
                       ha="center", va="top",
                       color="white", fontsize=10,
                       bbox={'facecolor': 'black', 'alpha': 0.5, 'pad': 5}
                       )
        # datetime object containing current date and time
             now = datetime.now()

        # dd/mm/YY H:M:S
             dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # Correct format of date and time 
   
             x = j   
             y= i - 0.35  # Adjust the y position for the current date and time 
             text_warning = ax.text(x,y,dt_string,ha="center", va="bottom", color="black",fontsize=6)

       # Calculate x and y coordinates for the warning text
             x_warning = j
             y_warning = i - 0.15  # Adjust the y position for the warning text
             if temperature_values[j] > 30:
                text_warning = ax.text(x_warning, y_warning, s="Status - High Temperature!", ha="center", va="bottom", color="b")
             else:
                 text_warning = ax.text(x_warning, y_warning, s="Status - Normal Temperature!", ha="center", va="bottom", color="r")
animation = FuncAnimation(fig, update_heatmap, interval=5000)  # Update every 5 seconds

# Continuously update temperature values
while True:
    update_heatmap(None)
    plt.pause(5)  # Update every 5 seconds
    
# Show the animated heatmap
plt.show()
