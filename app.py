import telebot
import random
from translate import translator
import os
from config import Config

config = Config()

bot = telebot.TeleBot(os.environ.get(config.env_key, None))
LANG_TO = 'be'
LANG_FROM = 'ru'
TIME_OFFSET = 120  # секунд до повторной отправки (5мин)


def translate(text, date):
    if date - config.old_date > TIME_OFFSET:
        try:
            translate_message = translator(LANG_FROM, LANG_TO, text)
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
    elif user in config.users:
        translate_text = translate(text, message.date)
        if translate_text:
            bot.send_message(chat_id, translate_text)
            config.old_date = message.date


bot.polling()
