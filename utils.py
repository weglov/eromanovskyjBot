import os
import random

from telebot import types
from translate import translator

from config import Config

config = Config()
fact_ending = os.environ.get(config.env_fact_end, None)


def with_remove(bot):
    def decorator_handler(fn):
        def wrapper(*args, **kw):
            body = args[0]

            if "-d" in body.text and body.text.startswith("/"):
                print(f"Triggering remove: {body.text} | {body.from_user.username}")

                try:
                    bot.delete_message(body.chat.id, body.message_id)
                except Exception:
                    print(f"Can't remove {body.chat.id} | {body.from_user.username}")

            return fn(*args, **kw)

        return wrapper

    return decorator_handler


def translate(text):
    try:
        translate_message = translator(config.lang_from, config.lang_to, text)
        return translate_message[0]
    except Exception:
        return


def get_fact():
    fact = random.choice(config.facts)
    return f"{fact.capitalize()} (c) {fact_ending}"


def check_press_button_user(call):
    chat_id = call.message.chat.id

    press_users = config.press_button[chat_id]["users"]
    if call.from_user.username in press_users:
        return True, False

    press_users.append(call.from_user.username)
    is_all = len(press_users) == config.users_count

    return False, is_all


def get_markup_pubg():
    markup = types.InlineKeyboardMarkup()

    row = [
        types.InlineKeyboardButton("Да", callback_data="yes"),
        types.InlineKeyboardButton("Нет", callback_data="no"),
    ]

    markup.row(*row)
    return markup


def update_text(call):
    text = call.message.text + "\n\n"
    user = call.from_user.first_name or "@" + call.from_user.username
    because = random.choice(config.because_i_am[call.data])

    return (
        text
        + f"{user}: Я {'пас' if call.data == 'no' else 'за'} потому что я {because}"
    )
