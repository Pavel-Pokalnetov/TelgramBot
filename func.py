from datetime import datetime
import requests


def calcrun(usrerexp):
    return eval(usrerexp)


def days2NY():
    now = datetime.today()
    NY = datetime(now.year + 1, 1, 1)
    d = NY-now
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)
    return ('До нового года: {} дней {} часа {} мин {} сек.'.format(d.days, hh, mm, ss))


def getweather():
    from config import APIKEY, CITY_ID
    try:
        responce = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={'id': CITY_ID, 'units': 'metric', 'lang': 'ru', 'APPID': APIKEY})
        data = responce.json()
        weather = "Погода в Cалехарде\nОблачность: {}\n".format(
            data['weather'][0]['description'])
        weather += "Температура: {} °С".format(data['main']['temp'])
        # print(weather)
        return (weather)
    except Exception as e:
        print("Exception (weather):", e)




def get_aurora():
    """прогноз полярных сияний
    https://services.swpc.noaa.gov/"""
    try:
        p = requests.get("https://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg")
        out = open("aurora.jpg", "wb")
        out.write(p.content)
        out.close()
    except:
        return(None)
    return("aurora.jpg")

if __name__== "__main__":
    aurora()