import telebot
from translate import translator
from config import Config

config = Config()

bot = telebot.TeleBot(config.token)
LANG_TO = 'be'
LANG_FROM = 'ru'
TIME_OFFSET = 2800 # секунд до повторной отправки (5мин)

def translate(text, date):
	if date - config.old_date > TIME_OFFSET:
		try:
			translate_message = translator(LANG_FROM, LANG_TO, text)
			return translate_message[0]
		except:
			print('Too many Requests')
	else:
		print('ждем еще')

def passExceptions():
	return "Парни сори, я пас, сегодня я каблук"

@bot.message_handler(content_types=['text'])
def send_text(message):
	user = message.from_user.username
	text = message.text
	chat_id = message.chat.id

	if message.text in ["-", "пас"]:
		bot.send_message(chat_id, passExceptions())
	elif user in ['eromanovskyj', 'dm_melnikov']:
		translate_text = translate(text, message.date)
		if translate_text:
			bot.send_message(chat_id, translate_text)
			config.old_date = message.date

bot.polling()

# TODO: захостить на хероку