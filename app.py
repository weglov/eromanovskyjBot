import telebot
import os
from config import Config
from messages import message_turbine

from utils import (
    check_press_button_user,
    get_markup_pubg,
    translate,
    update_text,
    with_remove,
)


config = Config()
bot = telebot.TeleBot(os.environ.get(config.env_key, None))


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
    msg, bot_msg_type, v = message_turbine(message)

    if not msg:
        return

    if bot_msg_type == 'sticker':
        bot.send_sticker(message.chat.id, msg)
    elif bot_msg_type == 'reply':
        bot.reply_to(message, msg)
    else:
        bot.send_message(message.chat.id, msg)


if __name__ == "__main__":
    bot.polling()
