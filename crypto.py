from binance.client import Client
from telegram import ParseMode
from telegram.ext import CommandHandler, Defaults, Updater
import pytz
from datetime import datetime
import config


client = Client(config.api_key, config.api_secret)

tz = pytz.timezone('Asia/Singapore')

def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='👋 Hello there! Welcome to Crypto Price Bot‼️')

def CoinPrice(update, context):
    if len(context.args) > 0:
        crypto = context.args[0].upper()

        current_price = client.get_symbol_ticker(symbol=crypto)["price"]

        response = f'The current price of {crypto} is {current_price} USDT.'
    else:
        response = f'Please check your inputs.'

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def PriceFeed(update, context):
    context.job_queue.run_repeating(PriceFeedCallback, interval=5, context=[update.message.chat_id, update.message.message_id])
    response = f"Price tracking started..."
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def PriceFeedCallback(context):
    if True==True:
        timestamp = datetime.now(tz)
        ethbtc = round(float(client.get_symbol_ticker(symbol="ETHBTC")["price"]), 6)
        btc = round(float(client.get_symbol_ticker(symbol="BTCUSDT")["price"]), 2)
        eth = round(float(client.get_symbol_ticker(symbol="ETHUSDT")["price"]), 2)
        
        response = f"ETHBTC: {ethbtc}\nBTCUSDT: {btc}\nETHUSDT: {eth}\n\n{timestamp}"

    context.bot.editMessageText(chat_id=context.job.context[0], message_id=context.job.context[1]+1, text=response)

if __name__ == '__main__':
    updater = Updater(token=config.telegram_token, defaults=Defaults(parse_mode=ParseMode.HTML))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', startCommand))
    dispatcher.add_handler(CommandHandler('p', CoinPrice))
    dispatcher.add_handler(CommandHandler('feed', PriceFeed))

    updater.start_polling() # Start the bot

    updater.idle() # Wait for the script to be stopped, this will stop the bot as well
