from datetime import datetime


class Config:
    env_key = 'TELE_KEY'
    lang_to = 'be'
    lang_from = 'ru'
    time_offset = 300 # секунд до повторной отправки (5мин)
    users = ['eromanovskyj', 'dm_melnikov']
    old_date = datetime.today().timestamp() - 280
    phrases = [
        "пернул мозгом",
        "да, ништяк",
        "хуй в кармане ночевал",
        "ключи от жопы потерял",
        "ебануться туфли гнутся",
        "кому тут отстрочить",
        "Пожил блять"
    ]