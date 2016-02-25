import sys
import telebot
import json
#from TwitterAPI import TwitterAPI
from telebot import types

# Create bot with its token

with open ("./acm.token","r") as TOKEN:
  bot = telebot.TeleBot(TOKEN.read())

# Authenticate on Twitter (@acmupm)
#with open ("./data/.twitter.json") as twitter:
#  t = json.load(twitter)
#  consumerKey = t['ConsumerK']
#  consumerSecret = t['ConsumerS']
#  accessToken = t['AccessT']
#  accessSecret = t['AccessS']

# Vars used
preciosTracking = {}
lmgtfyTracking = {}

# Functions used
def isUserAnswer(user, userTracking):
  if user in userTracking.keys():
    return True
  else:
    return False

def listener(messages):
  # When new messages arrive TeleBot will call this function.
  for m in messages:
    if m.content_type == 'text':
      # Prints the sent message to the console
      if m.chat.type == 'private':
        print ("Chat -> " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
      else:
        print ("Group -> " + str(m.chat.title) + " [" + str(m.chat.id) + "]: " + m.text)
    
# Initializing listener
bot.set_update_listener(listener) 

# Twitter login
#api = TwitterAPI(consumerKey, consumerSecret, accessToken, accessSecret)

# Files used
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

with open('./data/admins.json', 'r') as adminData:
  admins = json.load(adminData)

print("Running...")

# Custom keyboards
seleccionComida = types.ReplyKeyboardMarkup(one_time_keyboard=True)
seleccionComida.add('Bebida','Especiales')
seleccionComida.add('Comida','Todo')
seleccionComida.add('Cerrar')

lmgtfySearch = types.ReplyKeyboardMarkup(one_time_keyboard=True)
lmgtfySearch.add('Cancelar')

hideBoard = types.ReplyKeyboardHide()

# Handlers

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, welcome)

@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message, leHelp)

@bot.message_handler(commands=['quehaceacm'])
def send_info(message):
  bot.reply_to(message, info)

@bot.message_handler(commands=['precios'])
def send_precios_comida(message):
  chatId = message.chat.id
  bot.send_message(chatId, "Que precios quieres ver?", reply_markup=seleccionComida)
  preciosTracking[message.from_user.id] = message.chat.first_name

@bot.message_handler(func=lambda message: isUserAnswer(message.from_user.id, preciosTracking))
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

 preciosTracking.pop(message.from_user.id, None)

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
  if message.text == "/lmgtfy" or message.text == "/lmgtfy@acmupm_bot":
    bot.send_message(message.chat.id, "Que quieres que busque por ti?", reply_markup=lmgtfySearch)
    lmgtfyTracking[message.from_user.id] = message.chat.first_name
  else:
    lmgtfy_url = "http://lmgtfy.com/?q=" + "+".join(message.text.split()[1:])
    bot.reply_to(message, lmgtfy_url)

@bot.message_handler(func=lambda message: isUserAnswer(message.from_user.id, lmgtfyTracking))
def send_lmgtfyExtended(message):
  if message.text == 'Cancelar':
    bot.send_message(message.chat.id, "#sexyACM", reply_markup=hideBoard)
  else:
    lmgtfy_url = "http://lmgtfy.com/?q=" + "+".join(message.text.split())
    bot.reply_to(message, lmgtfy_url, reply_markup=hideBoard)

  lmgtfyTracking.pop(message.from_user.id, None)
  
@bot.message_handler(commands=['tldr'])
def send_tldr(message):
  GIF = open('./data/tldr.mp4', 'rb')
  bot.send_document(message.chat.id, GIF)

#@bot.message_handler(commands=['spam'])
#def send_spam(message):
#  if message.chat.type == 'private':
#    if str(message.from_user.id) in admins.keys():
#      text = message.text.split(' ', 1)[1]      
#      bot.send_message("@theIronChannel", text)
#      r = api.request('statuses/update', {'status': text})
#      print(r.status_code)
#    else:
#      bot.reply_to(message, "No eres un admin")
#  else:
#    bot.reply_to(message, "El spam solo se puede enviar por chat privado")

bot.polling()
