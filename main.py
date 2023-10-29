import telebot
import webbrowser
import json
import os

config = open("C:/Users/nabac/OneDrive/Desktop/bot-Telegram/config.json","r")
_config = json.loads(config.read())

bot = telebot.TeleBot(_config["token"])

@bot.message_handler(commands = ['site', 'website'])
def site(message):
    webbrowser.open('https://www.znu.edu.ua/ukr/university/11929')


@bot.message_handler(commands = ["start", "hello"])
def main(message): 
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}, я бот помощник Инженерного учебно-научного института</b>', parse_mode = 'html')


@bot.message_handler(commands = ["help"])
def main(message): 
    bot.send_message(message.chat.id, '<b>Все мои возможности: </b>', parse_mode = 'html')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}, я бот помощник Инженерного учебно-научного института</b>', parse_mode = 'html')
    elif message.text.lower() == "id":
        bot.reply_to(message, f'Твой ID: {message.from_user.id}')

bot.polling(none_stop = True)
