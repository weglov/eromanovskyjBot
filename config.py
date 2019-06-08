from datetime import datetime as dt

PHRASES = [
    "пернул мозгом",
    "да, ништяк",
    "хуй в кармане ночевал",
    "ключи от жопы потерял",
    "ебануться туфли гнутся",
    "кому тут отстрочить",
    "пожил блять",
    "вам жопу под хуи подставлять нужно, а не ...",
    "нелегальный пас",
    "там даже близко не было",
    "так резкий перевод темы",
    "неохото кассу маркину оставлять",
    "все верно",
    "принял понял, на хую пумпонил",
    "ебать дэпо дорогой",
    "sooooooqqaaaaaaaa",
    "парни, я же говорил что мы даже лучше общаться стали",
    "нормас",
    "так я напоминаю: https://www.youtube.com/watch?v=SHu8GSYIpwk",
    "так я напоминаю: https://www.youtube.com/watch?v=VhyaaPUeaYQ"
]


class PeriodConfig:
    translate_period = 3
    translate_count = 0
    last_message_data = dt.now().timestamp()

    punch_period = 15
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
