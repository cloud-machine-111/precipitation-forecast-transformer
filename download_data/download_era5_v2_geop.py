import cdsapi
import os
 
client = cdsapi.Client()
dataset = "reanalysis-era5-pressure-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": ["geopotential"],
    "year": ["1980"],
    "month": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
    "pressure_level": ["500"],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [0, -70, -60, -10],
    'grid': [0.25, 0.25],
}
def file_exists(path):
    return os.path.exists(path)

def make_request(year, month):
    file = "era5_data/amazon_geopotential/era5_amazon_geopotential_" + year + "_" + month + ".nc"
    print("trying " + file)
    if file_exists(file):
        print(file + " already exists")
    else:
        request["year"] = [year]
        request["month"] = [month]
        client.retrieve(dataset, request, file)
        print(file + " created")
    

years = [str(year) for year in range(1981, 2020)]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


for year in years:
    for month in months:
        make_request(year, month)