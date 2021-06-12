import logging
import os
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard

logging.basicConfig(format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "1499537994:AAHudM62Ej7jX_rFYCTl2xnj1sXsCRVgBAk"

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello!"

@app.route(f'/{TOKEN}', methods = ['GET', 'POST'])
def webhook():
	update = Update.de_json(request.get_json(), bot)
	dp.process_update(update)
	return "ok"


def start(bot, update):
	print(update)
	author=update.message.from_user.first_name
	reply = f"Hi! {author}"
	bot.send_message(chat_id = update.message.chat_id, text=reply)

def _help(bot, update):
	print(update)	
	help_txt = "Hey! This is help text. Isn't it helpful?"
	bot.send_message(chat_id = update.message.chat_id, text=help_txt)

def news(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = 'Choose a category', 
		reply_markup = ReplyKeyboardMarkup(keyboard = topics_keyboard, one_time_keyboard = True))

def reply_text(bot, update):
	# print(update)	
	# reply = update.message.text
	# bot.send_message(chat_id = update.message.chat_id, text=reply)
	print("here")
	intent, reply = get_reply(update.message.text, update.message.chat_id)
	if intent == "get_news":
		articles = fetch_news(reply)
		for article in articles:
			bot.send_message(chat_id=update.message.chat_id, text=article['link'])
	else:
		bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot, update):
	print(update)
	bot.send_sticker(chat_id = update.message.chat_id, sticker = update.message.sticker.file_id)

def error(bot, update):
	logger.error(f"Update {update} caused error {update.error}")

# def main():										# This was when making poller bot, the bot will
													# continuously ask the server for any requests, not
													# optimal when lots of users, webhook means now the server
													# will send the request to the url and you dont have to 
													# continuously query it!
	# updater = Updater(TOKEN)
	# dp = updater.dispatcher

	# dp = Dispatcher(bot, None)

	# dp.add_handler(CommandHandler("start", start))
	# dp.add_handler(CommandHandler("help", _help))
	# dp.add_handler(MessageHandler(Filters.text, echo_text))
	# dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
	# dp.add_error_handler(error)

	# updater.start_polling()
	# logger.info("Started Polling!")
	# updater.idle()

bot = Bot(TOKEN)

try:
	bot.set_webhook(os.environ.get("WEBHOOK_URL") + TOKEN)
except Exception as e:
	print(e)

dp = Dispatcher(bot, None)

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", _help))
dp.add_handler(CommandHandler("news", news))
dp.add_handler(MessageHandler(Filters.text, reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)


if __name__=='__main__':

	app.run(port = os.environ.get("PORT", 3333));
