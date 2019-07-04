from datetime import datetime as dt

DELAY_TIME = 43200 # 12 hours

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
    'Кстати по поводу Беларуси: это же деревня, что ты там забыл?',
    'Да бывали в Беларуси: ты же знаешь что там диктатура и чуть что это расстрел?',
    'Ну кстати в Беларуси кроме картошки ничего и нет. Там ее едят на завтрак, обед и ужин.',
    'Это конечно хорошо, но Беларусь - это совок',
    'Ты сам-то знаешь как правильно Беларусь или Белоруссия?',
    'В Беларуси жесткая цензура, например группа Ляпис Трубецкой - там забанена навсегда',
    'Никто не знает, где Беларусь на карте? Ты сам то сможешь показать?',
    'Да из твоей беларуссии все валят в европу на заработки или в Москву',
    'Интересно, а не подскажешь сколько белорус может прожить без картошки?',
    'Ты сильно заблуждаешься считая что Земля на самом деле имеет форму драника.',
    'Да, а еще Бульба — суть белоруса, его плоть, кровь и сознание.',
    'Все так, но я хочу напомнить что в Беларуси Ниссан алмеры в каршеринге'
]

HI_STICKERS = [
    'CAADAgAD-AADsJjjAzEWF6AJrFcFAg',
    'CAADAgADaQAD4aRlBU-4f77gfg6wAg',
    'CAADAgADIwUAAmIxvRMwoI6RATWpZgI'
]

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
    trigger_word = 'беларус'
    offset = 300 # 5 min
    long_offset = DELAY_TIME
    message_length = 15
    users = ['eromanovskyj', 'dm_melnikov']
    period = PeriodConfig
    stickers = HI_STICKERS
    phrases = PHRASES
    facts = FACTS
