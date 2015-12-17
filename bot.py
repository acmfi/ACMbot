import telebot

bot = telebot.TeleBot("92880306:AAHx-oybgswhlloA_hFxpBBvknBltoAyaV0")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Te damos al bienvenida al bot de ACM.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
bot.polling()
