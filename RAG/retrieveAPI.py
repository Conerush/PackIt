from flask import Flask,request
from rag import *
import json
import requests


app = Flask(__name__)
@app.route('/' , methods = ['GET' , 'POST'])
def index():
    return "Hello World!!!!"



@app.route('/api/get-packages' , methods = ['GET' , 'POST'])
def get_packages():
    if(request.method == 'POST'):
        request_data = request.get_json()
        return retrieve(request_data["description"], 10)



if __name__ == "__main__":
    app.run(debug=True)
