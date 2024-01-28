from flask import Flask,render_template,request,abort
import json
import urllib.request


app = Flask(__name__)
def tocelcius(temp):
    return str(round(float(temp) - 273.16,2))

@app.route('/',methods=['POST','GET'])
def weather():
    api_key = 'ef864563f67b6b77a069d7d372f19693'
    if request.method == 'POST':
        city = request.form['city']
    else:
        
        city = 'Songkhla'

    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
    except:
        return abort(404)
    

    list_of_data = json.loads(source)

    
    data = {
        "temp": str(list_of_data['main']['temp']) + 'k',
        "temp_cel": tocelcius(list_of_data['main']['temp']) + 'C',
        "humidity": str(list_of_data['main']['humidity']) + '%',
        
    }
    return render_template('index.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)