import numpy as np
import geocoder
import time

def filter_data(data):
    """
    Filters data for years after 2010 and data originating
    from Syria.

    Inputs:
        data (pd.DataFrame): Input data with column "Year" and "Origin"
    Returns:
        data (pd.DataFrame): Filtered data
    """
    if 'Origin' in data.columns:
        data = data[(data.Year > 2010) & (data.Origin.str.contains('Syria'))]
    else:
        data = data[(data.Year > 2010)]
    return data


def str2num(data):
    """
    For each object type column check if any entry starts and
    ends with a digit. Replace * with np.nan since it's
    noted * is used to mask confidential information.
    Convert those columns to float type.

    Inputs:
        data (pd.DataFrame): Input data
    Returns:
        data (pd.DataFrame): Input data with correct dtypes
    """
    columns = data.select_dtypes(['object']).columns
    for c in columns:
        if data[c].str.contains('^\d*\d$', regex=True).any():
            print(f'Converting column : {c}')
            data[c] = data[c].replace('*', np.nan).astype(np.float)
    return data


def latlng(q):
    """
    Geocode a given address

    Inputs:
        q (str): Input query for geocoding
    Returns:
        res.latlng (list): Latitude Longitude list
    """
    res = geocoder.google(q)
    while res.status != 'OK':
        print(res.status, q)
        time.sleep(2)
        res = geocoder.google(q)
    return res.latlng

def col2dt(data, columns):
    """Convert Year, Month, Day to Pandas Datetime"""
    # extract datetime from Year Month
    data = data.copy()
    date = ""
    for c in columns:
        date += (data[c].astype(str) + "/")
    date = date.apply(lambda x: x[:-1])
    data["date"] = pd.to_datetime(date)
    return data