from datetime import datetime as dt

PHRASES = [
    "Пернул мозгом",
    "Да, ништяк",
    "Хуй в кармане ночевал",
    "Ключи от жопы потерял",
    "Ебануться туфли гнутся",
    "Кому тут отстрочить",
    "Пожил блять",
    "Вам жопу под хуи подставлять нужно, а не ...",
    "Нелегальный пас",
    "Там даже близко не было",
    "Так резкий перевод темы",
    "Неохото кассу маркину оставлять",
    "Все верно",
    "Принял понял, на хую пумпонил",
    "Ебать дэпо дорогой",
    "Sooooooqqaaaaaaaa",
    "Парни, я же говорил что мы даже лучше общаться стали",
    "Нормас",
    "Так я напоминаю: https://www.youtube.com/watch?v=SHu8GSYIpwk",
    "Так я напоминаю: https://www.youtube.com/watch?v=VhyaaPUeaYQ"
]


class PeriodConfig:
    translate_period = 5
    translate_count = 0
    last_message_data = dt.now().timestamp()

    punch_period = 10
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
