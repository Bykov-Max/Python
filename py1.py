import telebot
from telebot import types
import sqlite3
import bd
from newsapi import NewsApiClient
import datetime
import requests
bd.connect()


name = ""
password = ""



now = datetime.datetime.now()
api_key_news='a7cd7377d93e495bab8a19f92a520134'



newsapi = NewsApiClient(api_key=api_key_news)


bot = telebot.TeleBot("2012584863:AAEI30dtIKEC7FPJKMHIYmHJIUkS1Yjq5ic")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
        bot.reply_to(message, "Привет, я бот!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
        if message.text == "Регистрация":
                bot.send_message(message.chat.id, "Привет! Давай познакомимся! Придумай пароль")
                bot.register_next_step_handler(message, reg)
        
        elif(message.text == "Войти"):
                bot.send_message(message.chat.id, "Введите пароль")
                bot.register_next_step_handler(message, auth)
        
        elif(message.text == "Подписки"):
                bot.send_message(message.chat.id, "Ваши подписки: ")
                answer=news(message.from_user.id)
                bot.send_message(message.chat.id, answer)
        
        elif(message.text == "Подписаться"):
                add = "Введите цифру, чтобы подписаться на категорию:\n 1 - Фильмы и сериалы \n 2 - Музыка \n 3 - Спорт \n 4 - Игры \n 5 - Сериалы"

                bot.send_message(message.chat.id, add)
                bot.register_next_step_handler(message, checkSub)
        
        elif(message.text == "Отписаться"):
                delete = "Введите цифру, чтобы отписаться от категории:\n 1 - Фильмы и сериалы \n 2 - Музыка \n 3 - Спорт \n 4 - Игры \n 5 - Сериалы"

                bot.send_message(message.chat.id, delete)
                bot.register_next_step_handler(message, delSubs)

        elif(message.text == "Новости"):
                showNewses = showNews(message.from_user.id)
                bot.send_message(message.chat.id, showNewses)
                
                

def checkSub(message):
        sub = message.text
        
        if sub == "1":
                answer = addSub(user_id = message.from_user.id, category_id = 1)
                bot.send_message(message.chat.id, answer)
                
        elif sub == "2":
                answer=addSub(user_id = message.from_user.id, category_id = 2)
                bot.send_message(message.chat.id, answer)

                        

        elif sub == "3":
                answer=addSub(user_id = message.from_user.id, category_id = 3)
                bot.send_message(message.chat.id, answer)


        elif sub == "4":
                answer=addSub(user_id = message.from_user.id, category_id = 4)
                bot.send_message(message.chat.id, answer)


        elif sub == "5":
                answer=addSub(user_id = message.from_user.id, category_id = 5)
                bot.send_message(message.chat.id, answer)
                                        


def delSubs(message):
        sub = message.text
        
        if sub == "1":
                answer = delSub(user_id = message.from_user.id, category_id = 1)
                bot.send_message(message.chat.id, answer)
                
        elif sub == "2":
                answer=delSub(user_id = message.from_user.id, category_id = 2)
                bot.send_message(message.chat.id, answer)
                        

        elif sub == "3":
                answer=delSub(user_id = message.from_user.id, category_id = 3)
                bot.send_message(message.chat.id, answer)


        elif sub == "4":
                answer=delSub(user_id = message.from_user.id, category_id = 4)
                bot.send_message(message.chat.id, answer)


        elif sub == "5":
                answer=delSub(user_id = message.from_user.id, category_id = 5)
                bot.send_message(message.chat.id, answer)


# def check(message):
#         user_id = bd.checkUser(user_id = message.from_user.id)
#         if user_id == 0:
#                 bot.register_next_step_handler(message, reg)
#         else:
#                 bot.send_message(message.chat.id, "Вы уже регистрировались")
        
        


def reg(message):
        global name, password, user_id
        url='http://127.0.0.1:5000/register'
        data={
                'user_id ': f'{message.from_user.id}',
                'password' : f"{message.text}",
                'name' : f'{message.from_user.first_name}'
        }
        

        response = requests.post(url, json=data)

        if response.status_code == 200:
                bot.send_message(message.chat.id, "Вы уже регистрировались")
        elif response.status_code == 201:
                bot.send_message(message.chat.id, "Регистрация прошла успешно")



def auth(message):
        global password, user_id
        response = requests.post('http://127.0.0.1:5000/auth', data={
                'user_id ': message.from_user.id,
                'password' : message.text,
        })

        if response.status_code == 200:
                bot.send_message(message.chat.id, "Вы вошли в систему")


def news(id):
        sub = bd.news(id)
        print (sub)
        abc=''
        for news in sub:
               abc+=news[0]+' '
        return abc

                
def addSub(user_id, category_id):
        addSub = bd.addSub(user_id, category_id)
        return addSub


def delSub(user_id, category_id):
        delSub = bd.delSub(user_id, category_id)
        return delSub


def showNews(user_id):
        sub = bd.news(user_id)
        print(sub)
        for subs in sub:
                url = (f"https://newsapi.org/v2/everything?q={subs[0]}&apiKey={api_key_news}&from={now.date}&sortBy=popularity?&language=ru&totalResults=5&pageSize=5")
                response = requests.get(url)
                response = response.json()

                print(response)

                try:
                        lists = 0
                        for i in range(0, len(response)+1):
                                title = response['articles'][i]['title']
                                href = response['articles'][i]['url']
                                lists += 1

                        if lists <=6:
                                bot.send_message(user_id, f"<a href='{href}'>{title}</a>", parse_mode="html")

                except KeyError as k:
                                print("------------------------")
                                print(k)
                

if __name__ == "__main__":
        bot.polling()