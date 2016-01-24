import sys
import telebot
import json
from telebot import types

def listener(messages):
  # When new messages arrive TeleBot will call this function.
  for m in messages:
    if m.content_type == 'text':
      # Prints the sent message to the console
      if m.chat.type == 'private':
       print ("Chat -> " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
      else:
       print ("Chat -> " + str(m.chat.title) + " [" + str(m.chat.id) + "]: " + m.text)

knownUsers = []
userStep = {}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
      knownUsers.append(uid)
      userStep[uid] = 0
      print ("Nuevo usuario que no ha usado \"/start\" todavia")
      return 0

with open ("./acm.token","r") as TOKEN:
  bot = telebot.TeleBot(TOKEN.read())

bot.set_update_listener(listener) # Este es el listener

with open('./data/data.json', 'r') as data:
  j = json.load(data)
  info = j['info']
  welcome = j['bienvenida']
  leHelp = j['help']
  events = j['events']
  reto = j['reto']
  bebida = j['bebida']
  comida = j['comida']
  especiales = j['especiales']

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

seleccionComida = types.ReplyKeyboardMarkup(one_time_keyboard=True)
seleccionComida.add('Bebida','Especiales')
seleccionComida.add('Comida','Todo')
seleccionComida.add('Cerrar')

hideBoard = types.ReplyKeyboardHide()

@bot.message_handler(commands=['precios'])
def send_precios_comida(message):
  chatId = message.chat.id
  bot.send_message(chatId, "Que precios quieres ver?", reply_markup=seleccionComida)
  userStep[chatId] = 1 # Esperando una contestacion

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_seleccion_precio(message):
  chatId = message.chat.id
  text = message.text

  if text == 'Bebida':
    bot.send_message(chatId, bebida, reply_markup=hideBoard)
  elif text == 'Comida':
    bot.send_message(chatId, comida, reply_markup=hideBoard)
  elif text == 'Especiales':
    bot.send_message(chatId, especiales, reply_markup=hideBoard)
  elif text == 'Todo':
    photo = open('./data/listaComida.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, reply_markup=hideBoard)
  else:
    bot.send_message(chatId, "#sexyACM", reply_markup=hideBoard)

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
  if(message.text == ""):
    markup = types.ForceReply(selective=True)
    bot.send_message(message.chat.id, "Que quieres que busque por ti?", reply_markup=markup)
    bot.register_next_step_handler(msg)
    lmgtfy_url = "http://lmgtfy.com/?q=" + "+".join(msg.text.split()[1:])
  else:
    lmgtfy_url = "http://lmgtfy.com/?q=" + "+".join(message.text.split()[1:])
    bot.reply_to(message, lmgtfy_url)

@bot.message_handler(commands=['tldr'])
def send_tldr(message):
  GIF = open('./data/tldr.mp4', 'rb')
  bot.send_document(message.chat.id, GIF)

bot.polling()
