import telebot
import random
from translate import translator
import os
from config import Config
from collections import namedtuple


config = Config()
bot = telebot.TeleBot(os.environ.get(config.env_key, None))

message_types = namedtuple('MessageType', 'translate, punch, skip')(
    'translate', 'punch', 'skip')

SKIP_MESS = "Парни сори, я пас, сегодня я каблук"


def _is_translate_time(message):
    if all([
        config.period.translate_count > config.period.translate_period,
        message.date - config.period.last_message_data > config.offset,
        len(message.text) > config.message_length,
    ]):
        config.period.translate_count = 0
        config.period.last_message_data = message.date
        return True
    return False


def _is_punch_time(message):
    if all([
        config.period.punch_count > config.period.punch_period,
        message.date - config.period.last_punch_data > config.offset,
    ]):
        config.period.punch_count = 0
        config.period.last_punch_data = message.date
        return True
    return False


def spot_answer_type(message):
    if message.text.lower() in ["-", "пас", "я пас"]:
        return message_types.skip

    elif message.from_user.username in config.users:
        return message_types.translate if _is_translate_time(message) else None

    return message_types.punch if _is_punch_time(message) else None


def translate(text):
    try:
        translate_message = translator(config.lang_from, config.lang_to, text)
        return translate_message[0]
    except Exception:
        return


@bot.message_handler(commands=['punch'])
def send_punch(message):
    bot.send_message(message.chat.id, random.choice(config.phrases).capitalize())


@bot.message_handler(content_types=['text'])
def send_text(message):
    config.period.punch_count += 1
    config.period.translate_count += 1 if message.from_user.username in config.users else 0

    type_ = spot_answer_type(message)

    mess = None
    if type_ == message_types.translate:
        mess = translate(message.text)

    elif type_ == message_types.punch:
        mess = random.choice(config.phrases)

    elif type_ == message_types.skip:
        mess = SKIP_MESS

    if mess:
        bot.send_message(message.chat.id, mess)


if __name__ == "__main__":
    bot.polling()
