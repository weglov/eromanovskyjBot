import os
import random

from telebot import types
from translate import translator

from config import Config, message_types

config = Config()
fact_ending = os.environ.get(config.env_fact_end, None)


def with_remove(bot):
    def decorator_handler(fn):
        def wrapper(*args, **kw):
            body = args[0]

            if '-d' in body.text and body.text.startswith('/'):
                print(f"Triggering remove: {body.text} | {body.from_user.username}")

                try:
                    bot.delete_message(body.chat.id, body.message_id)
                except Exception:
                    print(f"Can't remove {body.chat.id} | {body.from_user.username}")

            return fn(*args, **kw)

        return wrapper

    return decorator_handler


def _is_translate_time(message):
    if all([
        config.period.translate_count > config.period.translate_period,
        message.date - config.period.last_message_data > config.offset,
        len(message.text) > config.message_length,
        not message.text.startswith('http'),
    ]):
        return True
    return False


def _is_punch_time(message):
    if all([
        config.period.punch_count > config.period.punch_period,
        message.date - config.period.last_punch_data > config.offset,
    ]):
        return True
    return False


def _is_fact_time(message):
    return message.date - config.period.last_fact_data > config.long_offset


def _is_comapany_punch_time(message, detect_company):
    out_of_period = message.date - config.period.last_fact_data > config.long_offset

    return config.last_company_punch != detect_company and out_of_period


def _get_company_punch(message):
    text = message.text.lower()

    for company_key, company in config.company_triger.items():
        if any([word in text for word in company['matches']]):
            return company_key, company

    return None, None


def create_bot_msg(type=None, msg=None, reply=False):
    return type, msg, reply


def select_bot_answer(message):
    text = message.text.lower()
    _company_key, _company_items = _get_company_punch(message)

    if text in config.skip_triger:
        return create_bot_msg(message_types.skip, config.skip_mess)

    elif config.fight_triger in text.split(' '):
        return create_bot_msg(message_types.fight, config.fight_mess, reply=True)

    elif _company_key and _is_comapany_punch_time(message, _company_key):
        config.last_company_punch = _company_key
        return create_bot_msg(message_types.company, _company_items['punch'], reply=True)

    elif all([
        message.from_user.username not in config.users,
        any([word in text.split(' ') for word in config.ping_trigger]),
    ]):
        return create_bot_msg(message_types.ping, config.ping_mess)

    # logic only for special users
    elif message.from_user.username in config.users:
        if any([word in text for word in config.fact_triger]) and _is_fact_time(message):
            return create_bot_msg(message_types.fact, get_fact(), True)

        if _is_translate_time(message):
            return create_bot_msg(message_types.translate, translate(message.text))

    if _is_punch_time(message):
        return create_bot_msg(message_types.punch, random.choice(config.phrases))

    return create_bot_msg()


def translate(text):
    try:
        translate_message = translator(config.lang_from, config.lang_to, text)
        return translate_message[0]
    except Exception:
        return


def get_fact():
    fact = random.choice(config.facts)
    return f"{fact.capitalize()} (c) {fact_ending}"


def reset_period(date):
    config.period.punch_count = config.period.translate_count = 0
    config.period.last_message_data = config.period.last_punch_data = date


def check_press_button_user(call):
    chat_id = call.message.chat.id

    press_users = config.press_button[chat_id]['users']
    if call.from_user.username in press_users:
        return True, False

    press_users.append(call.from_user.username)
    is_all = len(press_users) == config.users_count

    return False, is_all


def get_markup_pubg():
    markup = types.InlineKeyboardMarkup()

    row = [
        types.InlineKeyboardButton('Да', callback_data='yes'),
        types.InlineKeyboardButton('Нет', callback_data='no'),
    ]

    markup.row(*row)
    return markup


def update_text(call):
    text = call.message.text + '\n\n'
    user = call.from_user.first_name or "@" + call.from_user.username
    because = random.choice(config.because_i_am[call.data])

    return text + f"{user}: Я {'пас' if call.data == 'no' else 'за'} потому что я {because}"
