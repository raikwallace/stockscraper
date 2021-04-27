import logging
import threading
import uuid
import sys
from telegram.ext import Updater
from telegram.ext import CommandHandler
from stockscrapy.scrapy_interface import ScrapyInterface
from stockscrapy.stockscrapy.spiders.stock_spider import StockSpider
from settings import TOKEN, URLS, TIME_MAX_BETWEEN_EXECS_MS, TIME_MIN_BETWEEN_EXECS_MS, LOGGING_LEVEL

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=LOGGING_LEVEL)


class StockScraperBot():

    def __init__(self, admin_uuid):
        self.admin_uuid = admin_uuid
        self.admin_id = None
        self.updater = Updater(token=TOKEN, use_context=True)
        self.clients = {}
        self.config()
        self.spiders = {}
        self.scrapy_interface = ScrapyInterface()

    def config(self):
        dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        dispatcher.add_handler(start_handler)
        start_spider_handler = CommandHandler(
            'start_spider', self.start_spider)
        dispatcher.add_handler(start_spider_handler)
        join_handler = CommandHandler('join', self.join)
        dispatcher.add_handler(join_handler)
        unjoin_handler = CommandHandler('unjoin', self.unjoin)
        dispatcher.add_handler(unjoin_handler)
        help_handler = CommandHandler('help', self.help)
        dispatcher.add_handler(help_handler)
        shutdown_handler = CommandHandler('shutdown', self.shutdown)
        dispatcher.add_handler(shutdown_handler)

        self.clients["3080Ti"] = []
        self.clients["3080"] = []
        self.clients["3070"] = []

    def run(self):
        self.updater.start_polling()

    def start(self, update, context):
        if context.args[0] == self.admin_uuid:
            self.default_context = context
            self.admin_id = update.effective_chat.id
            self.send_text_message(
                update.effective_chat.id, 'You have been added as administrator of this bot.', context)
        else:
            self.send_text_message(
                update.effective_chat.id, 'This command requires administrator permissions.', context)

    def start_spider(self, update, context):
        if update.effective_chat.id == self.admin_id:
            results=[]
            t = threading.Thread(target=self.scrapy_interface.run_spider_with_scheduler, args=(results,
                                                                                  self.is_there_stock, StockSpider, URLS[context.args[0]]), kwargs={'time_min_between_execs_ms': TIME_MIN_BETWEEN_EXECS_MS, 'time_max_between_execs_ms': TIME_MAX_BETWEEN_EXECS_MS}, daemon=True)
            t.start()
            self.spiders[context.args[0]] = t
            self.send_text_message(
                update.effective_chat.id, 'The spider for ' + context.args[0] + " has started.", context)
        else:
            self.send_text_message(
                update.effective_chat.id, 'This command requires administrator permissions.', context)

    def join(self, update, context):
        if self.spiders.get(context.args[0]) == None :
            self.send_text_message(
                update.effective_chat.id, 'The list for RTX '+context.args[0]+' doesn\'t exist or is inactive.', context)
            return
        if self.clients[context.args[0]].count(update.effective_chat.id) > 0 :
            self.send_text_message(
                update.effective_chat.id, 'You already are member of this list.', context)
            return
        try:
            self.clients[context.args[0]].append(update.effective_chat.id)
            self.send_text_message(
                update.effective_chat.id, 'You have been added to the list for RTX '+context.args[0], context)
        except:
            self.send_text_message(
                update.effective_chat.id, 'You can\'t join that list.', context)

    def unjoin(self, update, context):
        try :
            self.clients[context.args[0]].remove(update.effective_chat.id)
            self.send_text_message(
                update.effective_chat.id, 'You have been removed from the list for RTX '+context.args[0], context)
        except:
            self.send_text_message(
                update.effective_chat.id, 'You can\'t unjoin that list.', context)

    def help(self, update, context):
        self.send_text_message(
            update.effective_chat.id, 'StockScraperBot v1.0.0 \n This bot looks for stock at the NVIDIA shop for the RTX 3070, 3080 and 3080Ti FE graphic cards. \n The bot\'s commands are the following: \n - /join [3070|3080|3080Ti] - Activate notifications for the stock of the indicated graphic card \n - /unjoin [3070|3080|3080Ti] - Deactivate the notifications for the indicated graphic card \n - /help - Show this text', context)

    def stop(self):
        self.updater.stop()
        self.updater.is_idle = False

    def shutdown(self, update, context):
        if update.effective_chat.id == self.admin_id:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Shutting down bot...")
            threading.Thread(target=self.stop).start()
        else:
            self.send_text_message(
                update.effective_chat.id, 'This command requires administrator permissions.', context)

    def is_there_stock(self, results):
        group = ""
        logging.log(logging.INFO, 'results:' + str(results))
        for g, url in URLS.items():
            if(url == results.get("url")):
                group = g
        if(results.get("buy") != None and results.get("buy") != 'AGOTADO'):
            logging.log(logging.INFO, '🎉🎉🎉 There is stock for ' +
                        group + ' 🎉🎉🎉 \n Link: ' + URLS[group])
            self.notificate(group)
        return False  # To continue running spider

    def notificate(self, group):
        self.send_text_message_to_group(
            group, '🎉🎉🎉 There is stock for ' + group + ' 🎉🎉🎉 \n Link: ' + URLS[group], self.default_context)

    def send_text_message_to_group(self, group, text, context):
        for chat_id in self.clients[group]:
            context.bot.send_message(chat_id=chat_id, text=text)

    def send_text_message(self, chat_id, text, context):
        context.bot.send_message(
            chat_id=chat_id, text=text)


if __name__ == '__main__':
    admin_uuid = str(uuid.uuid4())
    logging.log(logging.WARNING, "The admin code is: " + admin_uuid +
                " . Please, send it to the bot with the /start command to set your chat as administrator one.")
    stockscraper_bot = StockScraperBot(admin_uuid)
    stockscraper_bot.run()
