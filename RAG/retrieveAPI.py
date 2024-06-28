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
    results = []
    if(request.method == 'POST'):
        request_data = request.get_json()
        data = retrieve(request_data["description"], 10)

        for name in data:
            results.append(name["Name"])

        return results



if __name__ == "__main__":
    app.run(debug=True)
