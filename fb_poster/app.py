import socialbot
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods = ['POST'])
def main():
    socialbot.execute(request.json)
    data = {'message': 'Created', 'code': 'SUCCESS'}
    return data, 200