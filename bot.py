import telebot
import json

bot = telebot.TeleBot("92880306:AAHx-oybgswhlloA_hFxpBBvknBltoAyaV0")

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
    
bot.polling()
