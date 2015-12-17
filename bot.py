import telebot

bot = telebot.TeleBot("92880306:AAHx-oybgswhlloA_hFxpBBvknBltoAyaV0")

with open('./data/QueHaceACM.txt', 'r') as myfile:
  info = myfile.read()

print("Running...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, "¡Hola! Te damos al bienvenida al bot de ACM.")

@bot.message_handler(commands=['queHaceACM'])
def send_info(message):
  bot.reply_to(message, info)
    
bot.polling()
