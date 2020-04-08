import random
import types
from datetime import datetime as dt
from inspect import signature
from typing import List, Any, Dict, Union, Optional, Callable

from typing_extensions import Literal


class Trigger:
    def __init__(self,
                 chance: int,
                 condition: List[Callable],
                 text: Union[Callable[[str], Any], str],
                 chance_step: int = 10,
                 command: Optional[str] = None,
                 bot_type: Optional[Literal['instant', 'reply', 'sticker']] = 'instant',
                 ) -> None:
        self.chance = chance
        self.command = command
        self.chance_step = chance_step
        self.current_chance = chance
        self.condition = condition
        self.text = text
        self.status = [False for i in condition]
        self.type = bot_type
        self.last_trigger = None

    def debug(self) -> Dict:
        return {
            'chance': self.current_chance,
            'status': self.status,
            'last_trigger': self.last_trigger
        }

    def get_message(self, msg) -> str:
        if isinstance(self.text, types.FunctionType):
            sig = signature(self.text)

            if len(sig.parameters):
                return self.text(msg)
            else:
                return self.text()

        return self.text

    def reset(self) -> None:
        self.status = [False for i in self.condition]
        self.current_chance = self.chance

    def check_condition(self, msg):
        for key, cond in enumerate(self.condition):
            self.status[key] = cond(msg)

        if all(x for x in self.status):
            rand = random.randrange(0, 100)

            if rand <= self.current_chance:
                self.reset()
                return True
            else:
                self.current_chance = self.current_chance + self.chance_step
                return False

        return False

    def is_command(self, msg) -> bool:
        if self.command:
            return msg.text.lower().startswith('/{}'.format(self.command))

        return False

    def on(self, msg):
        if self.is_command(msg) or self.check_condition(msg):
            self.last_trigger = dt.now().strftime('%Y-%m-%d-%H.%M.%S')
            return self

        return None
