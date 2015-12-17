import telebot

bot = telebot.TeleBot("92880306:AAHx-oybgswhlloA_hFxpBBvknBltoAyaV0")

with open('./data/QueHaceACM.txt', 'r') as knowUs_file:
  info = knowUs_file.read()

with open('./data/bienvenida.txt', 'r') as welcome_file:
  welcome = welcome_file.read()
  
print("Running...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, welcome)

@bot.message_handler(commands=['quehaceacm'])
def send_info(message):
  bot.reply_to(message, info)
    
bot.polling()
