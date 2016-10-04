import sys
import telebot
import json
# from TwitterAPI import TwitterAPI
from telebot import types
import os.path as path

# Create bot with its token
if not path.isfile("acm.token"):
    print("Error: \"acm.token\" not found!")
    sys.exit()

with open("./acm.token", "r") as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Ignorar mensajes antiguos
bot.skip_pending = True

# Functions used


def isAdmin_fromPrivate(message):
    if message.chat.type == 'private':
        userID = message.from_user.id
        if str(userID) in admins:
            return True
    return False


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
                print("Chat -> " + str(m.chat.first_name) +
                      " [" + str(m.chat.id) + "]: " + m.text)
        else:
            print("Group -> " + str(m.chat.title) +
                  " [" + str(m.chat.id) + "]: " + m.text)

# Initializing listener
#bot.set_update_listener(listener)

# Files used
if not path.isfile("./data/data.json"):
    with open('./data/data.json', 'w') as data:
        data.write('{}')
        data.close

with open('./data/data.json', 'r') as data:
    j = json.load(data)
    global info
    info = j['info']
    global welcome
    welcome = j['bienvenida']
    global events
    events = j['events']
    global reto
    reto = j['reto']
    global bebida
    bebida = j['bebida']
    global comida
    comida = j['comida']
    global especiales
    especiales = j['especiales']

if not path.isfile("./data/groups.json"):
    with open("./data/groups.json", "w") as groups:
        groups.write("{}")
        groups.close

with open('./data/groups.json', 'r') as groups:
    global groupsData
    groupsData = json.load(groups)
    
if not path.isfile("./data/help.json"):
    with open('./data/help.json', 'w') as leHelp:
        leHelp.write('{}')
        leHelp.close

with open('./data/help.json', 'r') as leHelp:
    helpData = json.load(leHelp)

helpMessage = "Estos son los comandos disponibles:\n\n"
for key in helpData:
    helpMessage += "- /" + key + " :: "
    helpMessage += helpData[key] + "\n"

if not path.isfile("./data/admins.json"):
    with open('./data/admins.json', 'w') as adminData:
        adminData.write('{}')
        adminData.close

with open('./data/admins.json', 'r') as adminData:
    admins = json.load(adminData)

print("Running...")

# Handlers


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, welcome)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, helpMessage)


@bot.message_handler(commands=['quehaceacm'])
def send_info(message):
    bot.send_message(message.from_user.id, info)


@bot.message_handler(commands=['eventos'])
def send_events(message):
    if events == '':
        GIF = open('./data/carlton.mp4', 'rb')
        bot.send_message(message.from_user.id, 'No hay eventos!')
        bot.send_document(message.from_user.id, GIF)
    else:
        bot.send_message(message.from_user.id, events)


@bot.message_handler(commands=['reto'])
def send_challenge(message):
    bot.send_message(message.from_user.id, "El reto de esta semana es:\n\n" + reto)

# Inline handler


@bot.inline_handler(lambda query: query.query.lower() == 'precios')
def precios_inline(iq):
    r_comida = types.InlineQueryResultArticle('1', 'Comida', types.InputTextMessageContent(comida))
    r_bebida = types.InlineQueryResultArticle('2', 'Bebida', types.InputTextMessageContent(bebida))
    r_especiales = types.InlineQueryResultArticle('3', 'Especiales', types.InputTextMessageContent(especiales))
    bot.answer_inline_query(iq.id, [r_comida, r_bebida, r_especiales])

# Only admins!!


@bot.message_handler(commands=['update'])
def auto_update(message):
    if isAdmin_fromPrivate(message):
        bot.reply_to(message, "Reiniciando..\n\nPrueba algun comando en 10 segundos")
        print("Updating..")
        sys.exit()
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")


@bot.message_handler(commands=['newreto'])
def new_challenge(message):
    if isAdmin_fromPrivate(message):
        url_reto = message.text.split(' ', 1)[1]
        j['reto'] = url_reto
        with open('./data/data.json', 'w') as dataW:
            dataW.write(json.dumps(j))
        bot.reply_to(message, "El nuevo reto es:\n\n" + url_reto)
        print("Updating..")
        with open('./data/data.json', 'r') as data:
            j2 = json.load(data)
            global reto
            reto = j2['reto']
        print("Updated")
    else:
        bot.reply_to(message, "Este comando es solo para admins y debe ser enviado por privado")


@bot.message_handler(commands=['groupsinfo'])
def groups(m):
    toSend = ""
    for key in groupsData.keys():
        toSend += "*Grupo:* " + key
        toSend += "\n  _Admin:_ " + str(groupsData[key]["admin"])
        toSend += "\n  _Descripcion:_ " + str(groupsData[key]["description"]) + "\n\n"

    bot.send_message(m.from_user.id, toSend, parse_mode="Markdown")


@bot.message_handler(content_types=['new_chat_member'])
def welcome(m):
    user = m.new_chat_member.username
    bot.send_message(m.chat.id, "Bienvenido @" + user + " !!\nSoy el bot de ACM-UPM, puedes invocarme desde aquí poniendo /help@acmupm_bot o cualquier otro comando, pero te contestaré por privado. Para que pueda contestarte por privado manda a @acmupm_bot el comando /start directamente!")
    
# Start the bot
bot.polling()
