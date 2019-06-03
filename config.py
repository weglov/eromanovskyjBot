from datetime import datetime as dt

PHRASES = [
    "пернул мозгом",
    "да, ништяк",
    "хуй в кармане ночевал",
    "ключи от жопы потерял",
    "ебануться туфли гнутся",
    "кому тут отстрочить",
    "Пожил блять",
]


class PeriodConfig:
    translate_period = 3
    translate_count = 0
    last_message_data = dt.now().timestamp()

    punch_period = 25
    punch_count = 0
    last_punch_data = dt.now().timestamp()


class Config:
    env_key = 'TELE_KEY'
    lang_to = 'be'
    lang_from = 'ru'
    offset = 300
    message_length = 15
    users = ['eromanovskyj', 'dm_melnikov']
    phrases = PHRASES
    period = PeriodConfig
