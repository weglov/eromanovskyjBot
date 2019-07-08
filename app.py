import telebot
import random
import os
from config import Config

from utils import (
    get_fact,
    message_types,
    reset_period,
    spot_answer_type,
    translate,
)


config = Config()
bot = telebot.TeleBot(os.environ.get(config.env_key, None))


@bot.message_handler(commands=['punch'])
def send_punch(message):
    phrase = random.choice(config.phrases).capitalize()

    bot.send_message(message.chat.id, phrase)


@bot.message_handler(commands=['sayhialbert'])
def send_hi(message):
    sticker = random.choice(config.stickers)
    bot.send_sticker(message.chat.id, sticker)


@bot.message_handler(commands=['fact'])
def send_fact(message):
    fact = get_fact()

    bot.send_message(message.chat.id, fact)


@bot.message_handler(content_types=['text'])
def send_text(message):
    config.period.punch_count += 1
    config.period.translate_count += 1 if message.from_user.username in config.users else 0

    type_ = spot_answer_type(message)

    mess = None
    if type_ == message_types.fact:
        bot.reply_to(message, get_fact())

    if type_ == message_types.translate:
        mess = translate(message.text)

    elif type_ == message_types.punch:
        mess = random.choice(config.phrases)

    elif type_ == message_types.skip:
        mess = config.skip_mess

    if mess:
        bot.send_message(message.chat.id, mess)
        reset_period(message.date)


if __name__ == "__main__":
    bot.polling()
