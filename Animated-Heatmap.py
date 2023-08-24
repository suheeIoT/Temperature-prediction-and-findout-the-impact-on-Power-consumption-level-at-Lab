import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np

# Function to read temperature data from a CSV file
def read_temperature_data1(file_path):
    data1 = pd.read_csv(file_path)
    data1.columns = ['Date','Temperature'] 
    dates1 = pd.to_datetime(data1['Date'],format='ISO8601')
    temperature_data1 = data1['Temperature']
    return dates1, temperature_data1

# Function to read temperature data from a  2nd CSV file
def read_temperature_data2(file_path):
    data2 = pd.read_csv(file_path)
    data2.columns = ['Date','Temperature'] 
    dates2 = pd.to_datetime(data2['Date'],format='ISO8601')
    temperature_data2 = data2['Temperature']
    return dates2, temperature_data2

# Function to update the temperature heatmap
def update_temperature_heatmap1(frame):
    dates1, temperature_data1 = read_temperature_data1(r'C:\Nokia_Project\Temperatures_DB.csv')
    start_index1 = frame * heatmap_rows1 * heatmap_cols1
    end_index1 = start_index1 + heatmap_rows1 * heatmap_cols1
    heatmap1.set_array(temperature_data1[start_index1:end_index1].values.reshape(heatmap1.get_array().shape))
    ax1.set_xticklabels(dates1[start_index1:end_index1].dt.strftime('%Y-%m-%d %H:%M:%S'), rotation=45)
    return [heatmap1]

# Function to update the temperature heatmap2
def update_temperature_heatmap2(frame):
    dates2, temperature_data2 = read_temperature_data2(r'C:\Nokia_Project\Temperatures.csv')
    start_index = frame * heatmap_rows2 * heatmap_cols2
    end_index = start_index + heatmap_rows2 * heatmap_cols2
    heatmap2.set_array(temperature_data2[start_index:end_index].values.reshape(heatmap2.get_array().shape))
    ax2.set_xticklabels(dates2[start_index:end_index].dt.strftime('%Y-%m-%d %H:%M:%S'), rotation=45)
    return [heatmap2]

# Read initial temperature data from the CSV file
dates1, temperature_data1 = read_temperature_data1(r'C:\Nokia_Project\Temperatures_DB.csv')

# Read initial temperature data from the CSV file
dates2, temperature_data2 = read_temperature_data1(r'C:\Nokia_Project\Temperatures.csv')

# Determine the dimensions of the heatmap
heatmap_rows1 = 300  # Number of rows in the heatmap
num_frames1 = 60
heatmap_cols1 = int(len(temperature_data1) / num_frames1 / heatmap_rows1)  # Number of columns in the heatmap
#num_frames = (heatmap_rows * heatmap_cols)  # Number of frames calcultion
num_frames1 = int(len(temperature_data1) / (heatmap_rows1 * heatmap_cols1))  # Number of frames based on the length of Temperature as well as rows & columns 

# Determine the dimensions of the heatmap2
heatmap_rows2 = 300  # Number of rows in the heatmap
num_frames2 = 60
heatmap_cols2 = int(len(temperature_data2) / num_frames2 / heatmap_rows2)  # Number of columns in the heatmap
#num_frames = (heatmap_rows * heatmap_cols)  # Number of frames calcultion
num_frames2 = int(len(temperature_data2) / (heatmap_rows2 * heatmap_cols2))  # Number of frames based on the length of Temperature as well as rows & columns 


# Create thefigure and axis
fig1, ax1 = plt.subplots()

# Create the 2nd figure and axis
fig2, ax2 = plt.subplots()

# Create the initial heatmap1
heatmap1 = ax1.imshow(np.zeros((heatmap_rows1, heatmap_cols1)), cmap='jet', interpolation='nearest', aspect='auto',vmin=22, vmax=32)
cbar = plt.colorbar(heatmap1)
ax1.set_title('Animated Temperature Variation- Region-A(FRANCE)')
ax1.set_xlabel('Date')
ax1.set_ylabel('No of Frames')

# Create the initial heatmap2
heatmap2 = ax2.imshow(np.zeros((heatmap_rows2, heatmap_cols2)), cmap='hot', interpolation='nearest', aspect='auto',vmin=22, vmax=32)
cbar = plt.colorbar(heatmap2)
ax2.set_title('Animated Temperature Variation- Region-B(FRANCE)')
ax2.set_xlabel('Date')
ax2.set_ylabel('No of Frames')

# Create the animation
animation1 = FuncAnimation(fig1, update_temperature_heatmap1, frames=num_frames1, interval=1000, blit=False)
# Create the  2nd animation
animation2 = FuncAnimation(fig2, update_temperature_heatmap2, frames=num_frames2, interval=1000, blit=False)

# Show the animated plot
plt.show()
