import telebot
import pytz
import os
from flask import Flask, request
from datetime import datetime
from constants import DATE_FORMAT, HELP_MESSAGE, TIME_FORMAT

TOKEN = os.environ['TOKEN']

bot = telebot.TeleBot(TOKEN, threaded=False)
server = Flask(__name__)
timezones = []
timezones_datetime = []

def get_datetimes_message(timezones, datetime_input):
	for timezone in timezones:
		timezone_info = pytz.timezone(timezone)
		timezone_info = datetime_input.astimezone(timezone_info)
		timezone_info_message = timezone_info.replace(tzinfo=None)
		timezone_info_message = timezone + ': ' + datetime.strftime(timezone_info_message, DATE_FORMAT + ' ' + TIME_FORMAT)

		if (timezone_info_message in(timezones_datetime)):
			continue
		else:
			timezones_datetime.append(timezone_info_message)
	
	return timezones_datetime

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.reply_to(message, "BASURAAAA")

@bot.message_handler(commands=['addtimezone'])
def add_timezone(message):
	new_timezone = ' '.join(message.text.split()[1:])

	if (new_timezone in(timezones)):
		bot.reply_to(message, "Timezone registered already!")
		return

	if (new_timezone in(pytz.all_timezones)):
		timezones.append(new_timezone)
		bot.reply_to(message, "done!")
	else:
		bot.reply_to(message, "Timezone not valid!")

@bot.message_handler(commands=['deltimezone'])
def delete_timezone(message):
	timezone = ' '.join(message.text.split()[1:])

	if (timezone in(timezones)):
		timezones.remove(timezone)
		bot.reply_to(message, "done!")
	else:
		bot.reply_to(message, "Timezone not valid!")

@bot.message_handler(commands=['schedulegameplay'])
def schedule(message):
	game = message.text.split()[1]

	date = message.text.split()[2]
	try:
		datetime.strptime(date, DATE_FORMAT)
	except ValueError:
		bot.send_message(message.chat.id, "Invalid date format")
		return

	time = message.text.split()[3]
	try:
		datetime.strptime(time, TIME_FORMAT)
	except ValueError:
		bot.send_message(message.chat.id, "Invalid time format")
		return
	
	input_timezone = message.text.split()[4]
	try:
		pytz.timezone(input_timezone)
	except ValueError:
		bot.send_message(message.chat.id, "Invalid timezone")
		return

	datetime_string = ' '.join([date, time])
	timezone_input_info = pytz.timezone(input_timezone)
	datetime_object = datetime.strptime(datetime_string, DATE_FORMAT + ' ' + TIME_FORMAT)
	result_message = "Scheduled gameplay for " + game + " at the following date and time: \n \n"
	result_datetimes = '\n'.join(get_datetimes_message(timezones, timezone_input_info.localize(datetime_object)))

	bot.send_message(message.chat.id, result_message + result_datetimes)
	result_datetimes = ''

@bot.message_handler(commands=['timezones'])
def show_timezones(message):
	if not timezones:
		bot.reply_to(message, "No time zones registered")
	else:
		bot.send_message(message.chat.id, '\n'.join(timezones))

@bot.message_handler(commands=['help'])
def help(message):
	bot.reply_to(message, HELP_MESSAGE)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

# SERVER SIDE
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "Updated", 200

@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://limitless-lake-47905.herokuapp.com/' + TOKEN)
   return "Running", 200

if __name__ == "__main__":
	server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

bot.infinity_polling()
