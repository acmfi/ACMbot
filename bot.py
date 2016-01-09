import telebot
import json
from telebot import types

bot = telebot.TeleBot("92880306:AAFmwCI80R60hhHRcGNDl8m7Z-Oz5e_GqXE")

with open('./data/data.json', 'r') as data:
  j = json.load(data)
  info = j['info']
  welcome = j['bienvenida']

print("Running...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, welcome)

@bot.message_handler(commands=['quehaceacm'])
def send_info(message):
  bot.reply_to(message, info)

@bot.message_handler(commands=['comida'])
def send_precios(message):
  photo = open('./data/listaComida.jpg', 'rb')
  bot.send_photo(message.chat.id, photo)
  
bot.polling()
