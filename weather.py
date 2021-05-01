import requests
import json
import settings

daily = "https://api.weather.gov/gridpoints/SHV/39,67/forecast"
hourly = "https://api.weather.gov/gridpoints/SHV/39,67/forecast/hourly"
headers = {"personalPythonApp": "cisneros.jorge82@yahoo.com"}

def getRequest(req, headers):
    """
        Return Get Request
    """
    getRequest = requests.get(req, headers=headers)
    while getRequest.status_code != 200:
        getRequest = requests.get(req, headers=headers)
    return getRequest

def jsonRequest(req):
    """
        Grab JSON info from Request
    """
    j = json.loads(req.text)
    return j['properties']['periods']

def dailyForecast():
    """
        Print Daily Forecast
    """
    req = getRequest(daily, headers)

    while True:
        try:
            jsun = jsonRequest(req)
        except KeyError:
            continue        
        else:
            break

    # print info 
    for i, _ in enumerate(jsun):
        if i < 2:
            print()
            info = jsun[i]["name"]
            temp = str(jsun[i]["temperature"]) + jsun[i]["temperatureUnit"]
            cast = jsun[i]["shortForecast"]
            print(f"~ {temp} ~ {cast}")

def hourlyForecast():
    """
        Print Hourly Forecast
    """
    req = getRequest(hourly, headers)
    
    while True:
        try:
            jsun = jsonRequest(req)
        except KeyError:
            continue        
        else:
            break

    # print info
    for i, _ in enumerate(jsun):
        if i <= 24:
            month = str(jsun[i]['startTime'])[5:7]
            day = str(jsun[i]['startTime'])[8:10]
            time = str(jsun[i]['startTime'])[11:16]
            temp = str(jsun[i]['temperature']) + jsun[i]['temperatureUnit']
            cast = jsun[i]['shortForecast']
            print(f"\t\t\t{month}/{day} ~ {time} ~ {temp}")

if __name__ == "__main__":
    settings.clear()
    dailyForecast()
