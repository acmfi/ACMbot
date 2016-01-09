import telebot
import json
from telebot import types

bot = telebot.TeleBot("TOKEN")

with open('./data/data.json', 'r') as data:
  j = json.load(data)
  info = j['info']
  welcome = j['bienvenida']
  leHelp = j['help']
  
print("Running...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, welcome)

@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message, leHelp)

@bot.message_handler(commands=['quehaceacm'])
def send_info(message):
  bot.reply_to(message, info)

@bot.message_handler(commands=['comida'])
def send_precios(message):
  photo = open('./data/listaComida.jpg', 'rb')
  bot.send_photo(message.chat.id, photo)
  
bot.polling()
