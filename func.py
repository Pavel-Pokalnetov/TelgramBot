from random import randint
from datetime import datetime
import sqlite3
import requests

def logger(txt,con=False):
    with open('bot.log','a',encoding='utf8') as logfile:
        logfile.writelines(txt+'\n')
        if con: print(txt)

def calcrun(usrerexp):
    return eval(usrerexp)


def days2NY():
    now = datetime.today()
    NY = datetime(now.year + 1, 1, 1)
    d = NY-now
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)
    return 'До нового года: {} дней {} часа {} мин {} сек.'.format(d.days, hh, mm, ss)


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
        p = requests.get(
            "https://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg")
        out = open("aurora.jpg", "wb")
        out.write(p.content)
        out.close()
    except:
        return None
    return "aurora.jpg"


def engrusdict()->str:
    randlist = ",".join(list([str(randint(0, 51380)) for _ in range(5)]))
    with sqlite3.connect('dict.db') as conn:
        cur = conn.cursor()
        request = f"""SELECT id,engword,rusword FROM dict WHERE id IN ({randlist});"""
        cur.execute(request)
        result = cur.fetchall()
    txt = ''
    for _, engword, rusword in result:
        txt +='**{}**\n - {}\n\n'.format(engword,rusword.replace('|','\n - '))
    return txt


if __name__ == "__main__":
    engrusdict()
    pass
