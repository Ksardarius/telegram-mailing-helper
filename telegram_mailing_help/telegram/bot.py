import logging
from datetime import datetime

from telegram.ext import CommandHandler
from telegram.ext import Updater

from telegram_mailing_help.db.dao import Dao, User, UserState

log = logging.getLogger("mailingBot")


class MailingBot:
    def __init__(self, config, db: Dao):
        self.db = db
        self.daemon = True
        self.updater = Updater(token=config.telegramToken)
        self.dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.commandStart)
        self.dispatcher.add_handler(start_handler)

    def commandStart(self, update, context):
        user = self.db.getUserByTelegramId(str(update.message.chat.id))
        if user is None or user.state != UserState.CONFIRMED.value:
            text = "Вы не найдены в базе данных бота, добаление требует обращение к куратору, пожалуйста попросите " \
                   "ответственного человека, чтобы вас добавили, до этого времени доступа до бота у вас не будет!"
            if user is None:
                user = User(
                    id=None,
                    telegram_id=str(update.message.chat.id),
                    name="%s %s" % (update.message.chat.first_name, update.message.chat.last_name),
                    state=UserState.NEW.value,
                    created=datetime.now().isoformat()
                )
                self.db.saveUser(user)
        else:
            text = "Приветствую вас, %s" % user.name
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    def start(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()
