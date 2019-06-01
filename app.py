import telebot
import random
from translate import translator
import os
from config import Config

config = Config()
bot = telebot.TeleBot(os.environ.get(config.env_key, None))


def translate(text, date):
    if date - config.old_date > config.time_offset:
        try:
            translate_message = translator(config.lang_from, config.lang_to, text)
            return translate_message[0]
        except:
            print('Too many Requests')
    else:
        print('ждем еще', config.old_date, date)
        return


def pass_exceptions():
    return "Парни сори, я пас, сегодня я каблук"


def random_punch():
    return random.choice(config.phrases)


@bot.message_handler(commands=['punch'])
def send_text(message):
    bot.send_message(message.chat.id, random_punch())


@bot.message_handler(content_types=['text'])
def send_text(message):
    user = message.from_user.username
    text = message.text
    chat_id = message.chat.id

    if message.text.lower() in ["-", "пас", "я пас"]:
        bot.send_message(chat_id, pass_exceptions())
    elif user in config.users and len(text) > 10:
        translate_text = translate(text, message.date)
        if translate_text:
            bot.send_message(chat_id, translate_text)
            config.old_date = message.date


bot.polling()
