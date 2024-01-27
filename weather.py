from flask import Flask,render_template,request,abort
import json
import urllib.request


app = Flask(__name__)
def tocelcius(temp):
    return str(round(float(temp) - 273.16,2))

@app.route('/')
def hello():
    return 'Hello, World!'