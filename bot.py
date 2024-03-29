import os
import os.path as path
import sys
import telebot
from telebot import types
import json
from collections import OrderedDict
import logging
from logging import config
import coloredlogs


# Create a logger object.
def setup_logging(
    default_path='logging_conf.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):

    logging.basicConfig(level=default_level)
    FORMAT = ""

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
            FORMAT = config["formatters"]["verbose"]["format"]
            os.environ["COLOREDLOGS_LOG_FORMAT"] = FORMAT
        logging.config.dictConfig(config)

    logger = logging.getLogger("ACMBot")
    coloredlogs.install(level=default_level, logger=logger)

    return logger


logger = setup_logging()


# Create bot with its token
if not path.isfile("acm.token"):
    logger.warning("Error: \"acm.token\" not found!")
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
                logger.info("Chat -> " + str(m.chat.first_name) +
                      " [" + str(m.chat.id) + "]: " + m.text)
            else:
                logger.info("Group -> " + str(m.chat.title) +
                      " [" + str(m.chat.id) + "]: " + m.text)

# Initializing listener
bot.set_update_listener(listener)

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
    global botPresentationInGroup
    botPresentationInGroup = j['botPresentationInGroup']
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

if not path.isfile("./data/junta.json"):
    with open('./data/junta.json', 'w') as junta:
        junta.write('{}')
        junta.close

with open('./data/junta.json', 'r') as junta:
    juntaData = json.load(junta, object_pairs_hook=OrderedDict)

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


@bot.message_handler(commands=['junta'])
def send_junta(message):
    juntaStr = "*Junta:*\n"
    for position in juntaData.keys():
        juntaStr += "\t\t*" + position + "*\n"
        for info in juntaData[position].keys():
            t = type(juntaData[position][info])
            if t is OrderedDict:
                juntaStr += "\t\t\t\t*" + info + "*\n"
                for member in juntaData[position][info].keys():
                    juntaStr += "\t\t\t\t\t\t_" + member + ":_\n"
                    for memberInfo in juntaData[position][info][member].keys():
                        if "id" not in memberInfo:
                            juntaStr += "\t\t\t\t\t\t\t\t_" + memberInfo + ":_  " + str(juntaData[position][info][member][memberInfo]) + "\n"
            else:
                juntaStr += "\t\t\t\t_" + info + ":_  " + str(juntaData[position][info]) + "\n"
        juntaStr += "\n"
    toSend = "La composición de la junta de ACM es:\n\n" + juntaStr + "\n\n"
    bot.send_message(message.from_user.id, toSend, parse_mode="Markdown")


@bot.message_handler(commands=['juntaPing'])
def ping_junta(message):
    user_msg = message.from_user
    userId = message.from_user.id
    user = ("@" + user_msg.username) if hasattr(user_msg, 'username') else (user_msg.name)

    msg2junta = ""
    if len(message.text.split(' ', 1)) > 1:
        msg2junta = message.text.split(' ', 1)[1]

    membersToPing = []
    for position in juntaData.keys():
        for info in juntaData[position].keys():
            t = type(juntaData[position][info])
            if t is OrderedDict:
                for member in juntaData[position][info].keys():
                    for memberInfo in juntaData[position][info][member].keys():
                        if "id" in memberInfo and juntaData[position][info][member][memberInfo] not in membersToPing:
                            membersToPing.append(juntaData[position][info][member][memberInfo])

    toSend = "El usuario: " + user
    #toSend += " , con id: " + str(userId)
    if msg2junta != "":
        toSend += " envió este mensaje para la junta:\n"
        toSend += "---------------------------\n"
        toSend += msg2junta
        toSend += "\n---------------------------\n" + "Fin del mensaje."
    else:
        toSend += " dió un toque a la junta"
    toSend += "\n\n"

    for member in membersToPing:
        bot.send_message(member, toSend, parse_mode="Markdown")


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
        logger.info("Updating..")
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
        logger.info("Updating..")
        with open('./data/data.json', 'r') as data:
            j2 = json.load(data)
            global reto
            reto = j2['reto']
        logger.info("Updated")
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
def send_welcome_new(m):
    user = "@" + m.new_chat_member.username if hasattr(m.new_chat_member, 'username') else m.new_chat_member.name
    bot.send_message(m.chat.id, "Bienvenido " + user + " !!\n" + botPresentationInGroup)


@bot.message_handler(content_types=['left_chat_member'])
def send_bye_left_user(m):
    left_user = m.left_chat_member
    user =  ("@" + left_user.username) if hasattr(left_user, 'username') else (left_user.name)
    bot.send_message(m.chat.id, "Gracias por pasar " + user + "!!\nEs una pena, siempre saludaba...")
    #bot.send_message(left_user.id, "Gracias por pasarte por el grupo de ACM!!\nEsperarmos volver a verte pronto.")

# Start the bot
logger.info("Running...")
bot.polling()
