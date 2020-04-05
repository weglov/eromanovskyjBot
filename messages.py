import random
from config import Config
import json
from datetime import datetime as dt
from typing import List, Dict
from enum import Enum
from trigger import Trigger

from utils import (
    get_fact,
    translate,
)

TURBINE = {}
config = Config()


def timer_minutes(minutes: int = 1440):
    recent_time = dt.now().timestamp()

    def wrapper(msg):
        nonlocal recent_time

        is_spend_time = msg.date - recent_time

        if is_spend_time > minutes * 60:
            recent_time = msg.date

            return True

        return False

    return wrapper


def only_user(users: List[str]):
    def wrapper(msg):
        return msg.from_user.username in users

    return wrapper


def text_contains(words: List[str]):
    def wrapper(msg):
        return any([word in msg.text.lower() for word in words])

    return wrapper


def message_more(length: int):
    def wrapper(msg):
        return all([len(msg.text.lower()) > length, not msg.text.startswith('http')])

    return wrapper


def only_manually():
    def wrapper(*args):
        return False

    return wrapper


class MessagesType(Enum):
    PUNCH = 'punch'
    TRANSLATE = 'translate'
    SKIP = 'skip'
    FACT = 'fact'
    FIGHT = 'fight'
    PING = 'ping'
    SAY_HI = 'say_hi_albert'
    COMPANY = 'company'
    DEBUG = 'debug'


messages: Dict[MessagesType, Trigger] = {
    MessagesType.PUNCH: Trigger(
        chance=20,
        command='punch',
        condition=[timer_minutes(2880), only_user(['eromanoskij'])],
        text=lambda x: random.choice(config.phrases),
        bot_type='reply'
    ),
    MessagesType.FACT: Trigger(
        chance=20,
        command='fact',
        condition=[
            text_contains(['беларус', 'минск', 'лукашенк', 'картош', 'картоха', 'мiнск', 'минcк', 'минсk']),
            timer_minutes(2880),
            only_user(['eromanoskij'])
        ],
        text=get_fact,
        bot_type='reply'
    ),
    MessagesType.FIGHT: Trigger(
        chance=50,
        condition=[timer_minutes(1440), text_contains(['бой'])],
        text='Мой хуй с твоей губой',
        bot_type='reply'
    ),
    MessagesType.TRANSLATE: Trigger(
        chance=50,
        condition=[
            timer_minutes(2880),
            message_more(100),
            only_user(['eromanoskij']),
        ],
        text=translate,
        bot_type='reply'
    ),
    MessagesType.SKIP: Trigger(
        chance=100,
        condition=[timer_minutes(2880), text_contains(['пас'])],
        text='Парни сори, я пас, сегодня я каблук',
        bot_type='reply'
    ),
    MessagesType.SAY_HI: Trigger(
        chance=100,
        command='sayhialbert',
        condition=[only_manually(), only_user(['eromanoskij', 'scheglov'])],
        text=lambda x: random.choice(config.stickers),
        bot_type='sticker'
    ),
    MessagesType.COMPANY: Trigger(
        chance=30,
        condition=[timer_minutes(1400), text_contains(['пас'])],
        text='Парни сори, я пас, сегодня я каблук',
        bot_type='reply'
    ),
    MessagesType.DEBUG: Trigger(
        chance=100,
        command='debug',
        condition=[only_manually(), only_user(['scheglov'])],
        text=lambda x: '{}'.format(json.dumps(TURBINE)),
        bot_type='reply'
    ),
}


def message_turbine(msg):
    for key in messages:
        TURBINE[str(key)] = messages[key].on(msg)

    for m in TURBINE:
        if TURBINE[m][0]:
            return TURBINE[m]

    return None, '', ''
