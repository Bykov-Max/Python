from flask import Flask
from flask import request
from flask import jsonify
import requests
import datetime
now = datetime.datetime.now()
import bd
from newsapi import NewsApiClient

api_key_news='a7cd7377d93e495bab8a19f92a520134'

newsapi = NewsApiClient(api_key=api_key_news)


app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    try:
        reg = bd.checkUser(request.form["user_id"])
        if reg == 1:
            return jsonify({"Вы уже регистрировались"}), 200
        else:
            bd.reg(request.form['user_id'], request.form["password"], request.form['name'])
            return jsonify({"Вы зарегистрированы"}), 201
    
    except Exception as e:
        print(f"Ошибка: {e}")
       


@app.route('/auth', methods=['POST'])
def auth():
    try:
        bd.reg(request.form['user_id'], request.form["password"])
        return jsonify({"Вы вошли в систему"}), 200
    
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    app.run()