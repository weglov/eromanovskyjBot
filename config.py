from datetime import datetime as dt
from collections import namedtuple

DELAY_TIME = 43200   # 12 hours

PHRASES = [
    'пернул мозгом',
    'да, ништяк',
    'хуй в кармане ночевал',
    'ключи от жопы потерял',
    'ебануться туфли гнутся',
    'кому тут отстрочить',
    'пожил блять',
    'вам жопу под хуи подставлять нужно, а не ...',
    'нелегальный пас',
    'там даже близко не было',
    'так резкий перевод темы',
    'неохото кассу маркину оставлять',
    'все верно',
    'принял понял, на хую пумпонил',
    'ебать дэпо дорогой',
    'sooooooqqaaaaaaaa',
    'парни, я же говорил что мы даже лучше общаться стали',
    'нормас'
]

# Disclaimer: below are humorous stereotypes, in fact, we love and respect Belarus ❤️
FACTS = [
    'кстати по поводу Беларуси: это же деревня, что ты там забыл?',
    'да бывали в Беларуси: ты же знаешь что там диктатура и чуть что это расстрел?',
    'ну кстати в Беларуси кроме картошки ничего и нет. Там ее едят на завтрак, обед и ужин.',
    'это конечно хорошо, но Беларусь - это совок',
    'ты сам-то знаешь как правильно Беларусь или Белоруссия?',
    'в Беларуси жесткая цензура, например группа Ляпис Трубецкой - там забанена навсегда',
    'никто не знает, где Беларусь на карте? Ты сам то сможешь показать?',
    'да из твоей беларуссии все валят в европу на заработки или в Москву',
    'интересно, а не подскажешь сколько белорус может прожить без картошки?',
    'ты сильно заблуждаешься считая что Земля на самом деле имеет форму драника.',
    'да, а еще Бульба — суть белоруса, его плоть, кровь и сознание.',
    'все так, но я хочу напомнить что в Беларуси Ниссан алмеры в каршеринге'
]

HI_STICKERS = [
    'CAADAgAD-AADsJjjAzEWF6AJrFcFAg',
    'CAADAgADaQAD4aRlBU-4f77gfg6wAg',
    'CAADAgADIwUAAmIxvRMwoI6RATWpZgI'
]

message_types = namedtuple('MessageType', 'translate, punch, skip, fact')(
    'translate', 'punch', 'skip', 'fact')


class PeriodConfig:
    translate_period = 5
    translate_count = 0
    last_message_data = dt.now().timestamp()

    punch_period = 10
    punch_count = 0
    last_punch_data = dt.now().timestamp()

    last_fact_data = dt.now().timestamp() - DELAY_TIME


class Config:
    env_key = 'TELE_KEY'
    env_fact_end = 'FACT_KEY'

    lang_to = 'be'
    lang_from = 'ru'

    offset = 300   # 5 min
    long_offset = DELAY_TIME

    users = ('eromanovskyj', 'dm_melnikov')
    skip_mess = 'Парни сори, я пас, сегодня я каблук'
    skip_triger = ('eromanovskyj-', 'пас', 'я пас')
    fact_triger = ('беларус', 'минск', 'лукашенк', 'картош', 'картоха')
    pubg_mess = 'Ну что пасаны может катку в PUBG?'
    message_length = 15

    because_i_am = {
        'no': ('пидор', 'белорус', 'каблук', 'лох', 'армянин', 'яндексоид'),
        'yes': ('белорус', 'армянин', 'яндексоид', 'красава', 'мужик', 'лучший'),
    }

    users_count = 3
    press_button_users = {}

    period = PeriodConfig
    stickers = HI_STICKERS
    phrases = PHRASES
    facts = FACTS
