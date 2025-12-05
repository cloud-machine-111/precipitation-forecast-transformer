import cdsapi
 
client = cdsapi.Client()
dataset = "reanalysis-era5-single-levels"
request = {
    "product_type": ["reanalysis"],
    "variable": [
        "2m_temperature",
        "soil_temperature_level_1"
    ],
    "year": [
        "1980"
    ],
    "month": [
        "01", 
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
    "data_format": "netcdf",
    "download_format": "zip",
    "area": [0, -70, -10, -60],
    'grid': [0.25, 0.25],
}

def make_request(year, month):
    request["year"] = [year]
    request["month"] = [month]
    file = "era5_data/era5_amazon_single_levels_" + year + "_" + month
    client.retrieve(dataset, request, file)
    

years = [str(year) for year in range(1981, 2020)]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


for year in years:
    for month in months:
        make_request(year, month)