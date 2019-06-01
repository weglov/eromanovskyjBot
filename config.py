from datetime import datetime


class Config:
    env_key = 'TELE_KEY'
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