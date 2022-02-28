import pandas as pd
import numpy as np

from . import constants as CN 

def load_data(data_url):
    """ 
    This functions reads the csv output from the given url
    args: url string from where to download the data
    returns: a pandas dataframe
    """
    #read the data now skipping the bad rows - not sure how to fix this and getting to the forecast part
    df = pd.read_csv(data_url, sep=";", header=0, skiprows=24)
    df.reset_index()
    return df

def clean_and_aggregate_data(df):
    """
    this function cleans up the dataframe and aggregates the 20 forecasts for precipitation and temperature.
    ARgs: dataframe downloaded from the url
    returns: cleaned  and aggregated dataframe
    """

    #first two rows after header indicate the units. we ignore and store all data after
    df  = df.iloc[2: , :]
    # make copy so can do manipulation
    newdf = df.copy()
    #change the types of all temp and precip columns to float since they are read as str. we need this for mean aggregation
    #we assume that we have strings that can be converted to float
    for col in CN.temp_cols:
        newdf[col] = newdf[col].apply(lambda x: float(x))
    for col in CN.precip_cols:
        newdf[col] = newdf[col].apply(lambda x: float(x))
    #replace all -999.0 with nan
    newdf.replace(-999.0, np.nan, inplace=True)
    #change the time column to store a date time value instead of string
    newdf["time"] = pd.to_datetime(newdf["time"], format = "%Y%m%d %H:%M")
    #breakup the date-time into date and time as we want to store this data in db in two different columns
    newdf["forecast_date"] = newdf["time"].apply(lambda x: x.date())
    newdf["forecast_time"] = newdf["time"].apply(lambda x: x.time())
    #average  the temperatures for all the readings for a particular date/time station
    #skipping nan
    newdf["mean_temp"] = newdf[CN.temp_cols].apply(lambda x: np.mean(x), axis=1)
    newdf["mean_precip"] = newdf[CN.precip_cols].apply(lambda x: np.mean(x), axis=1)
    #trim the dataframe to only keep the relevant columns
    newdf = newdf[CN.cols_keep]
    return newdf

def store_to_database(df, Forecast):
    """
    This function takes a dataframe and stores it in a Forecast object
    args: df: Dataframe storing all the records
          Forecast: model in which to store all these records
    returns: a string indicating success or failure of the bulk insert
    """
    
    #capture the start date of forecast
    start_date = df.iloc[0]["forecast_date"]
    df["start_date"] = start_date
    #rename the column names to the field names so we can do bulk insert
    df.columns = CN.field_names
    #convert to dict
    df = df.to_dict('records')
    if Forecast.objects.filter(start_date=start_date).exists():
        return f'Data already stored on the server for forecast date {start_date}. Please try downloading tomorrow.'
    # Bulk insert
    Forecast.objects.bulk_create([Forecast(**r) for r in df])
    return f"Data successfully stored in database for forecast date {start_date}"



