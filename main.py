import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from google.colab import files
import warnings
warnings.filterwarnings('ignore')
import calendar

def get_average_sales_heatmap():
  # Get store name
  STORE_NAME = input('Enter Store name: ')
  
  # Load data
  print('Please upload Sales and Traffic data in csv format: ')
  df = files.upload()
  #Get Transaction data
  df = list(df.keys())[0]
  df = pd.read_csv(df)
  
  # Get the dates
  START_DATE = pd.to_datetime(df['Date']).dt.date.min().strftime('%m-%Y')
  END_DATE = pd.to_datetime(df['Date']).dt.date.max().strftime('%m-%Y')
  
  
  # Check
  if not isinstance(df.index, pd.DatetimeIndex):
    df.index = pd.to_datetime(df.iloc[:,0])
    df = df.drop(columns=df.columns[0])
    df = df.rename(columns={'Ordered Product Sales': 'Sales'})
  
  df = df.iloc[:,[0]]
  df.iloc[:,0] = df.iloc[:,0].str.replace("$","").str.replace(",","").astype("float")
  
  
  
  cmap = LinearSegmentedColormap.from_list(
      name = "test",
      colors = ["red", "white", "green"]
  )
  
  df["year"] = df.index.year
  
  
  heatmap_data = pd.DataFrame(df
                              .groupby(["year", df.index.day_name()])
                              .Sales
                              .mean()
                              .unstack()
                              )
  
  heatmap_data = heatmap_data[['Monday',"Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]]
  plt.figure(figsize=(9,9))
  sns.heatmap(heatmap_data,
              annot=True,
              cmap=cmap,
              fmt="g"
              )
  plt.title(f"Average year by day of week for all years {START_DATE} - {END_DATE} // {STORE_NAME}", fontsize=20, fontdict=dict(weight="bold"))
  plt.savefig(f"{STORE_NAME}'s Weekday by year between {START_DATE} - {END_DATE}.png")
  
  
  
  cmap = LinearSegmentedColormap.from_list(
      name = "test",
      colors = ["red", "white", "green"]
  )
  
  
  df["month"] = df.index.month
  
  
  heatmap_data = pd.DataFrame(df.
                              groupby(["month", df.index.day_name()])
                              .Sales
                              .mean()
                              .unstack()
                              )
  
  heatmap_data = heatmap_data[[calendar.day_name[i] for i in range(7)]]
  plt.figure(figsize=(9,9))
  sns.heatmap(heatmap_data,
              annot=True,
              cmap=cmap,
              fmt="g"
              )
  plt.title(f"Average Sales Month vs Day of Week {START_DATE} - {END_DATE} // {STORE_NAME}", fontsize=20, fontdict=dict(weight="bold"))
  plt.savefig(f"{STORE_NAME}'s Weekday by Month between {START_DATE} - {END_DATE}.png")
  return None
