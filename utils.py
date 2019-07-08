import random
from translate import translator
import os
from config import Config
from collections import namedtuple


config = Config()
fact_ending = os.environ.get(config.env_fact_end, None)

message_types = namedtuple('MessageType', 'translate, punch, skip, fact')(
    'translate', 'punch', 'skip', 'fact')

SKIP_MESS = "Парни сори, я пас, сегодня я каблук"


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


def spot_answer_type(message):
    text = message.text.lower()
    if text in ["-", "пас", "я пас"]:
        return message_types.skip

    # logic only for special users
    elif message.from_user.username in config.users:
        if any([word in text for word in ('беларус', 'минск')]) and _is_fact_time(message):
            return message_types.fact

        return message_types.translate if _is_translate_time(message) else None

    return message_types.punch if _is_punch_time(message) else None


def translate(text):
    try:
        translate_message = translator(config.lang_from, config.lang_to, text)
        return translate_message[0]
    except Exception:
        return


def get_fact():
    fact = random.choice(config.facts)

    return '{} (c) {}'.format(fact, fact_ending)


def reset_period(date):
    config.period.punch_count = config.period.translate_count = 0
    config.period.last_message_data = config.period.last_punch_data = date
