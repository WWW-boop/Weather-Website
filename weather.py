import sqlite3
from flask import Flask, render_template, request, abort
import json
import urllib.request

app = Flask(__name__)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('weather.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    sql_create_weather_table = """CREATE TABLE IF NOT EXISTS weather (
                                    id INTEGER PRIMARY KEY,
                                    cityname TEXT NOT NULL,
                                    temp REAL NOT NULL,
                                    humidity REAL NOT NULL,
                                    wind_speed REAL NOT NULL
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_weather_table)
    except sqlite3.Error as e:
        print(e)

@app.route('/', methods=['POST', 'GET'])
def weather():
    api_key = 'ef864563f67b6b77a069d7d372f19693'
    if request.method == 'POST':
        country = request.form['country']
    else:
        country = 'Japan'

    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + country + '&appid=' + api_key).read()
    except:
        return abort(404)

    list_of_data = json.loads(source)

    cityname = str(country)
    temp = float(list_of_data['main']['temp'])
    humidity = float(list_of_data['main']['humidity'])
    wind_speed = float(list_of_data['wind']['speed'])

    conn = create_connection()
    with conn:
        create_table(conn)
        sql = ''' INSERT INTO weather(cityname,temp,humidity,wind_speed)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (cityname, temp, humidity, wind_speed))
        conn.commit()

    return render_template('index.html', data={
        "cityname": cityname,
        "temp": str(temp) + 'k',
        "temp_cel": tocelcius(temp) + 'C',
        "humidity": str(humidity) + '%',
        "wind_speed": str(wind_speed) + 'm/s'
    })

@app.route('/home')
def home():
    return render_template('home.html')

def tocelcius(temp):
    return str(round(float(temp) - 273.16, 2))


if __name__ == '__main__':
    app.run(debug=True)
