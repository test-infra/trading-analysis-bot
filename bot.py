import os
import telegram
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from binance.client import Client
from binance_trading_bot import utilities, analysis, visual, monitor, news

MANUAL_TEXT = """@trading\_analysis\_bot is a Telegram chatbot for data-driven analytics of crypto-market on Binance.
 *Features*
 - Technical indicators: MA, BB, Ichimoku, VRVP 
 - Orderflow: limit order book, trading heatmap
 - Market indexes: Bletchley, Bitwise, CRIX 
 - On-chain metrics: NVTS, MVRV Z-Score
 - Sentiment and development: Twitter, Reddit, GitHub
 - Trading sessions: New York, London, Tokyo, Sydney
 - Newsflow: curated articles
 - Project profiles: token distribution model
 - Customized notifications
 *Commands*
 - /t <market> <time-frame> <num-day> 
 Transactions volume versus price statistics. 
 The argument <time-frame> and <num-day> can be omitted. 
 Examples: /t qtumusdt bttbnb or /t bttbtc xlmusdt 4h 30.
 - /n - Newsflow.
 - /m - Market indexes.
 - /h - Trading sesions.
 *Supports*
 If you don't have an account yet please use the these links to register to [Binance](https://www.binance.com/?ref=13339920) or [Huobi](https://www.huobi.br.com/en-us/topic/invited/?invite_code=x93k3).
 Tipjar:
 - BTC: [1DrEMhMP5rAytKyKXRzc6szTcUX8bZzZgq](1DrEMhMP5rAytKyKXRzc6szTcUX8bZzZgq)
 - ETH: [0x3915D216f9Fc6ec08f956555e84385513dE5f214](0x3915D216f9Fc6ec08f956555e84385513dE5f214)
 - LTC: [LX8GJkGTZFmAA7puCyVp48333iQdCN6vca](LX8GJkGTZFmAA7puCyVp48333iQdCN6vca)
 *Contact*
 vanvuong.trinh@gmail.com"""

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
BINANCE_SECRET_KEY = os.environ['BINANCE_SECRET_KEY']
BINANCE_API_KEY = os.environ['BINANCE_API_KEY']

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

def t(bot,update,args):
    bot.send_chat_action(chat_id=update.message.chat_id, 
                         action=telegram.ChatAction.TYPING)
    marketList = utilities.get_market_list(client)['symbol'].tolist()
    for market in args:
        market = market.upper()
        if market not in marketList:
            market = market+'BTC'
        msg = analysis.scalp_analysis(client, market)
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
        try:
            TIME_FRAME = args[-2]
            TIME_FRAME_DURATION = int(args[-1])
        except Exception:
            TIME_FRAME = '1h'
            TIME_FRAME_DURATION = 3
        analysis.analysis_visual(client, 
                                 market, 
                                 TIME_FRAME, 
                                 TIME_FRAME_DURATION)
        bot.send_photo(chat_id=update.message.chat_id, 
                       photo=open(market+'.png', 'rb'))
                       
def n(bot,update):
    bot.send_chat_action(chat_id=update.message.chat_id, 
                         action=telegram.ChatAction.TYPING)
    msg = news.news()
    update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

def manual(bot,update):
    bot.send_message(chat_id=update.message.chat_id, 
                     text=MANUAL_TEXT, 
                     parse_mode=ParseMode.MARKDOWN, 
                     disable_web_page_preview=True)

def main():
    updater=Updater(TELEGRAM_TOKEN)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start", manual))
    dp.add_handler(CommandHandler("help", manual))
    dp.add_handler(CommandHandler("t", t, pass_args=True))
    dp.add_handler(CommandHandler("n", n))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
