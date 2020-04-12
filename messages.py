import json
import random
from datetime import datetime as dt
from enum import Enum
from typing import List, Dict, Callable

from config import Config
from trigger import Trigger
from utils import (
    get_fact,
    translate,
)

config = Config()


def timer_minutes(minutes: int = 1440):
    recent_time = int(dt.now().timestamp() - minutes * 60)

    def wrapper(msg):
        nonlocal recent_time
        is_spend_time = msg.date - recent_time
        print("closure:", recent_time, "msg", msg.date, is_spend_time > minutes * 60)

        if is_spend_time > minutes * 60:
            recent_time = msg.date

            return True

        return False

    return wrapper


def only_user(users: List[str]) -> Callable:
    def wrapper(msg):
        return msg.from_user.username in users

    return wrapper


def text_contains(words: List[str]) -> Callable:
    def wrapper(msg):
        return any([word in msg.text.lower() for word in words])

    return wrapper


def message_more(length: int) -> Callable:
    def wrapper(msg):
        return all([len(msg.text.lower()) > length, not msg.text.startswith("http")])

    return wrapper


def only_manually() -> Callable:
    def wrapper(*args):
        return False

    return wrapper


def debug():
    debug_dict = {}

    for m in messages:
        debug_dict[str(m)] = messages[m].debug()

    return ("{}".format(json.dumps(debug_dict)),)


class MessagesType(Enum):
    PUNCH = "punch"
    TRANSLATE = "translate"
    SKIP = "skip"
    FACT = "fact"
    FIGHT = "fight"
    PING = "ping"
    SAY_HI = "say_hi_albert"
    COMPANY = "company"
    DEBUG = "debug"


messages: Dict[MessagesType, Trigger] = {
    MessagesType.PUNCH: Trigger(
        chance=50,
        command="punch",
        condition=[only_user(["eromanoskij"]), timer_minutes(2880)],
        text=lambda: random.choice(config.phrases),
        bot_type="reply",
    ),
    MessagesType.FACT: Trigger(
        chance=50,
        command="fact",
        condition=[
            only_user(["eromanoskij"]),
            text_contains(
                [
                    "беларус",
                    "минск",
                    "лукашенк",
                    "картош",
                    "картоха",
                    "мiнск",
                    "минcк",
                    "минсk",
                ]
            ),
            timer_minutes(1440),
        ],
        text=get_fact,
        bot_type="reply",
    ),
    MessagesType.FIGHT: Trigger(
        chance=100,
        condition=[text_contains(["бой"]), timer_minutes(1440),],
        text=lambda: "Мой хуй с твоей губой",
        bot_type="reply",
    ),
    MessagesType.TRANSLATE: Trigger(
        chance=50,
        condition=[only_user(["eromanoskij"]), message_more(100), timer_minutes(2880),],
        text=translate,
        bot_type="reply",
    ),
    MessagesType.SKIP: Trigger(
        chance=100,
        condition=[text_contains(["пас"]), timer_minutes(2880)],
        text="Парни сори, я пас, сегодня я каблук",
        bot_type="reply",
    ),
    MessagesType.SAY_HI: Trigger(
        chance=100,
        command="sayhialbert",
        condition=[only_user(["eromanoskij", "scheglov"]), only_manually()],
        text=lambda: random.choice(config.stickers),
        bot_type="sticker",
    ),
    MessagesType.DEBUG: Trigger(
        chance=100,
        command="debug",
        condition=[only_user(["scheglov"]), only_manually()],
        text=debug,
        bot_type="reply",
    ),
}


def message_turbine(msg):
    sorted_by_chance = sorted(
        messages.items(), key=lambda item: item[1].current_chance, reverse=True
    )

    for (_, trigger) in sorted_by_chance:
        trigger_msg = trigger.on(msg)

        if trigger_msg:
            return trigger_msg

    return None
