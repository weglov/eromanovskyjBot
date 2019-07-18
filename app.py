import telebot
import random
import os
from config import Config

from utils import (
    check_press_button_user,
    get_fact,
    get_markup_pubg,
    message_types,
    reset_period,
    spot_answer_type,
    translate,
    update_text,
    with_remove
)


config = Config()
bot = telebot.TeleBot(os.environ.get(config.env_key, None))


@bot.message_handler(commands=['punch'])
@with_remove(bot)
def send_punch(message):
    phrase = random.choice(config.phrases).capitalize()
    bot.send_message(message.chat.id, phrase)


@bot.message_handler(commands=['sayhialbert'])
@with_remove(bot)
def send_hi(message):
    sticker = random.choice(config.stickers)
    bot.send_sticker(message.chat.id, sticker)


@bot.message_handler(commands=['fact'])
@with_remove(bot)
def send_fact(message):
    fact = get_fact()
    bot.send_message(message.chat.id, fact)


@bot.message_handler(commands=['pubg'])
@with_remove(bot)
def send_pubg_request(message):
    if message.chat.type == 'private':
        return

    chat_id = message.chat.id
    active_poll = config.press_button.pop(chat_id, None)

    if active_poll:
        bot.delete_message(chat_id, active_poll.get('message'))

    title = translate(
        config.pubg_mess) if message.from_user.username in config.users else config.pubg_mess

    mess = bot.send_message(chat_id, title, reply_markup=get_markup_pubg())

    config.press_button[chat_id] = {
        'message': mess.message_id,
        'users': []
    }


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def pubg_poll_call(call):
    chat_id = call.message.chat.id
    is_exists, is_all = check_press_button_user(call)

    if not is_exists:
        bot.delete_message(chat_id, config.press_button[chat_id]['message'])
        mess = bot.send_message(
            chat_id, update_text(call), reply_markup=None if is_all else get_markup_pubg(),
        )
        config.press_button[chat_id]['message'] = mess.message_id

    if is_all:
        config.press_button.pop(chat_id)

    bot.answer_callback_query(call.id, text="")


@bot.message_handler(content_types=['text'])
def send_text(message):
    config.period.punch_count += 1
    config.period.translate_count += 1 if message.from_user.username in config.users else 0

    type_ = spot_answer_type(message)

    mess = None
    if type_ == message_types.fact:
        bot.reply_to(message, get_fact())
        reset_period(message.date)

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
