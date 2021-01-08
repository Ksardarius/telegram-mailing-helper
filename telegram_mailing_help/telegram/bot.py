import logging
from datetime import datetime

from telegram import InlineKeyboardMarkup, \
    InlineKeyboardButton, Update, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram.ext import Updater

from telegram_mailing_help.db.dao import Dao, User, UserState
from telegram_mailing_help.logic.listPreparation import Preparation

log = logging.getLogger("mailingBot")


# unicode codes: https://apps.timwhitlock.info/emoji/tables/unicode
class MailingBot:
    def __init__(self, config, db: Dao, preparation: Preparation):
        self.db = db
        self.preparation = preparation
        self.daemon = True
        self.updater = Updater(token=config.telegramToken)
        self.dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.commandStart)
        self.dispatcher.add_handler(start_handler)
        getDispatchGroupNames_handler = CallbackQueryHandler(pattern=r"^get_dispatch_group_names$",
                                                             callback=self.getDispatchGroupNames)
        self.dispatcher.add_handler(getDispatchGroupNames_handler)
        getLinksFrom_handler = CallbackQueryHandler(pattern=r"^get_links_from: (.+)$", callback=self.getLinksFrom)
        self.dispatcher.add_handler(getLinksFrom_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(unknown_handler)

    def commandStart(self, update: Update, context):
        message = update.message or update.callback_query.message
        user = self.db.getUserByTelegramId(str(message.chat.id))
        if user is None or user.state != UserState.CONFIRMED.value:
            text = "Вы не найдены в базе данных бота, добаление требует обращение к куратору, пожалуйста попросите " \
                   "ответственного человека, чтобы вас добавили, до этого времени доступа до бота у вас не будет!"
            if user is None:
                user = User(
                    id=None,
                    telegram_id=str(message.chat.id),
                    name="%s %s" % (message.chat.first_name, message.chat.last_name),
                    state=UserState.NEW.value,
                    created=datetime.now().isoformat()
                )
                self.db.saveUser(user)
            message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Попробовать еще раз",
                                       callback_data="get_dispatch_group_names")]]))
        else:
            buttons = [[InlineKeyboardButton(text=groupName,
                                             callback_data="get_links_from: %s" % groupName)]
                       for groupName in self.db.getEnabledDispatchGroupNames()]
            if buttons:
                text = "Выберите рассылку из предложенных, %s:" % user.name
                message.reply_text(text,
                                   reply_markup=InlineKeyboardMarkup(buttons))
            else:
                text = "\U000026A0 На текущий момент нет ни одной активной рассылки, уточните почему, у куратора"
                message.reply_text(text, reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Попробовать еще раз",
                                           callback_data="get_dispatch_group_names")]]))
        if update.callback_query:
            update.callback_query.answer()

    @staticmethod
    def unknown(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Такую команду бот не поддерживает, попробуйте сначала /start")

    def getLinksFrom(self, update: Update, context):
        message = update.message or update.callback_query.message
        user = self.db.getUserByTelegramId(str(message.chat.id))
        if UserState(user.state) == UserState.CONFIRMED:
            dispatchListGroupName = update.callback_query.data[len("get_links_from: "):]
            text = self.preparation.getAndAssignDispatchList(user, dispatchListGroupName)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="<b style='text-align: center;'>%s:</b>" % dispatchListGroupName,
                                     parse_mode=ParseMode.HTML)
            update.callback_query.message.reply_text(text,
                                                     reply_markup=InlineKeyboardMarkup(
                                                         [
                                                             [InlineKeyboardButton(
                                                                 text="\U000027A1 %s: след. блок" % dispatchListGroupName,
                                                                 callback_data=update.callback_query.data)],
                                                             [InlineKeyboardButton(
                                                                 text="\U0001F4C3 Выбрать другой список",
                                                                 callback_data="get_dispatch_group_names")]
                                                         ]))
            update.callback_query.answer()
        else:
            message.reply_text("Получить данные не удалось, попробуйте позже или еще раз")

    def getDispatchGroupNames(self, update: Update, context):
        self.commandStart(update, context)

    def start(self):
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()
