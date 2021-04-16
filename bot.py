import logging
import threading
import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
from scraper import get_stock
from settings import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class StockScraperBot():
    
    def __init__(self):
        self.updater = Updater(token=TOKEN, use_context=True)
        self.clients={}
        self.config()
        self.scrapers=[]

    def config(self):
        dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        join_handler = CommandHandler('join', self.join)
        dispatcher.add_handler(join_handler)
        shutdown_handler = CommandHandler('shutdown', self.shutdown)
        dispatcher.add_handler(shutdown_handler)

        self.clients[3080]=[]
        self.clients[3070]=[]

    def start(self, update, context):
        t=threading.Thread(target=get_stock, args=(int(context.args[0]), self.send_text_message_to_group, context,), daemon=True)
        t.start()
        self.scrapers.append(t)
        self.send_text_message(update.effective_chat.id, 'Hi, this is @stockscraperbot. Please send /join to become a client of this bot and /unjoin to leave.', context)

    def join(self, update, context):
        self.clients[int(context.args[0])].append(update.effective_chat.id)
        self.send_text_message(update.effective_chat.id, 'You have been added to the list for RTX '+context.args[0], context)

    def send_text_message_to_group(self, group, text, context):
        for chat_id in self.clients[group] :
            context.bot.send_message(chat_id=chat_id, text=text)

    def send_text_message(self, chat_id, text, context):
        context.bot.send_message(
            chat_id=chat_id, text=text)

    def run(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()
        self.updater.is_idle = False

    def shutdown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="shutting down bot...")
        threading.Thread(target=self.stop).start()


if __name__ == '__main__':
    stockscraper_bot = StockScraperBot()
    stockscraper_bot.run()
