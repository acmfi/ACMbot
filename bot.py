import sys
import telebot
import json
from telebot import types

TOKEN = open('./token/acm.token', 'r')

bot = telebot.TeleBot(TOKEN.read())

TOKEN.close()

with open('./data/data.json', 'r') as data:
  j = json.load(data)
  info = j['info']
  welcome = j['bienvenida']
  leHelp = j['help']
  events = j['events']
  reto = j['reto']

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
def send_prices(message):
  photo = open('./data/listaComida.jpg', 'rb')
  bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['eventos'])
def send_events(message):
  if events == '':
    GIF = open('./data/carlton.mp4', 'rb')
    bot.send_message(message.chat.id, 'No hay eventos!')
    bot.send_document(message.chat.id, GIF)
  else:
    bot.reply_to(message, events)

@bot.message_handler(commands=['reto'])
def send_challenge(message):
  bot.reply_to(message, reto)  

@bot.message_handler(commands=['lmgtfy'])
def send_lmgtfy(message):
  lmgtfy_url = "http://lmgtfy.com/?q=" + "+".join(message.text.split()[1:])
  bot.reply_to(message, lmgtfy_url)

bot.polling()
