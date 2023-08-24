import matplotlib.colors as mc # Used to set a line color matlplot library
import matplotlib.pyplot as plt # Uses to make Matplotlib like Matlab . Eg- Create a figure, Decorate ..etc
import numpy as np # Perform numerical operation
import pandas as pd # Most suitable library for data cleaning and analysis in ML. Best tool for handling massy data

# Another utility for the legend
from matplotlib.cm import ScalarMappable # for colormap generation
import seaborn as sns # Used to visualize random distribution


data = pd.read_csv(r'C:\Nokia_Project\Temperatures_DB.csv', sep=',',   # Comma uses as a separator in this dataset
                 infer_datetime_format=True, 
                 low_memory=False, na_values=['nan','?'])

data = pd.DataFrame(data)  # Create a DataFrame using data as an inputs

print("TEMPERATURE DATA VISUALIZATION ")
print("-----------------------------------------------------------")

print("Please enter in between 1-6 for a Selection!")

print("Please enter 1 for visualizing data for entire period! ")
print("Please enter 2 for daily temperature variation! ")
print("Please enter 3 for hourly temperature variation!")


print("Please enter 4 for visualizing hourly Heatmap!  ")
print("Please enter 5 for visualizing daily Heatmap !")
print("Please enter 6 for visualizing monthly Heatmap!")

print("-----------------------------------------------------------")

Sel = input("Please enter your selection :")   # Getting input from user 

if (Sel =="1"):
    data.columns = ['Date','Temperature_at_NokiaLab']   # Define a columns for data. There is no column name at the data
    data.describe() # Some description about Temperature data to make sure about the column details 

#Resampling Process before analysis and visualization"""

    data['Date'] = pd.to_datetime(data['Date'],format='ISO8601')  # Conversion of string data into Datetime format & maintain ISO8601 standard

    #data_index = data.set_index('Date')   # 

    plt.figure(figsize=(15,6)) # Ploting Temperature for entire duration 
    sns.lineplot(x='Date',y='Temperature_at_NokiaLab',data=data,color='purple')
    #Define seaborn background colors and draw a line plot

    plt.title('Temperature Variation At Nokia Lab (Entire Period)')
    plt.show()


elif(Sel =="2"):
    data.columns = ['Date','Temperature_at_NokiaLab']   # Define a column for data
    data['Date'] = pd.to_datetime(data['Date'],format='ISO8601')  # Creating string data into Date time format

    df_day = data.resample('1D', on='Date',kind='period').mean()  # Ploting Temperature for one day & Selecting kind option uses to get only periodic value otherwise it will take timestamp value. Timestamp value represents in ugly format
    df_day.Temperature_at_NokiaLab.plot(title='Temperature Variation Per Day illustration', color='cyan') 
    plt.tight_layout()
    plt.show()

elif(Sel=="3"):
    data.columns = ['Date','Temperature_at_NokiaLab']   # Define a column for data
    data['Date'] = pd.to_datetime(data['Date'],format='ISO8601')  # creating string data into Date time format

    df_hour = data.resample('H', on='Date',kind='period').mean() # Ploting temperature in hourly format
    df_hour.Temperature_at_NokiaLab.plot(title='Temperature Variation VS Hourly illustration', color='green') 
    plt.tight_layout()
    plt.show()


# Heatmap Representation 
# Date format should be in Datetime format to perform heatmap analysis using pandas library

elif(Sel=="4"):
# Heatmap Representation for every hours 
    data.columns = ['Date','Temperature_at_NokiaLab']   # Define a column for data
    data['Date'] = pd.to_datetime(data['Date'],format='ISO8601')  # Creating string data into Date time format

    df_hm = data.resample('1H', on='Date',kind='period').mean()   # Consider only average value for a representation
    sns.heatmap(df_hm,annot=False,fmt=".1f",vmin=22, vmax=32,cmap='jet') # Annotation false means, it doesn’t show the aveg Temp value on the map& Temp range is defined in between 22 to 32 range
    plt.title(" Temperature Variation at Nokia Lab (Hourly) ")
   
    plt.show()

elif(Sel=="5"):
# Heatmap Representation for every week
    data.columns = ['Date','Temperature_at_NokiaLab']   # Define a column for data
    data['Date'] = pd.to_datetime(data['Date'],format='ISO8601')  # Creating string data into Date time format

    df_hm = data.resample('D', on='Date',kind='period').mean()
    sns.heatmap(df_hm,annot=True,fmt=".1f",vmin=22, vmax=32,cmap='jet',annot_kws={"size":10})
    plt.title(" Temperature Variation at Nokia Lab (Daily Variation) ")
   
    plt.show()

# Heatmap Representation for every Month
elif (Sel=="6"):
    data.columns = ['Date','Temperature_at_NokiaLab']   # Define a column for data
    data['Date'] = pd.to_datetime(data['Date'],format='ISO8601')  # Creating string data into Date time format

    df_hm = data.resample('M', on='Date',kind='period').mean()

    sns.heatmap(df_hm,annot=True,fmt=".1f",vmin=22, vmax=32,cmap='jet',annot_kws={"size":10})
    plt.title(" Temperature Variation at Nokia Lab (Monthly Variation) ")
   
    plt.show()

else:

    print("Invalid Selection! Please Select The Correct Range!!")  # Else statement for ending a clauses
