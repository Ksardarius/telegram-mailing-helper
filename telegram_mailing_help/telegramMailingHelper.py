# /usr/bin/env poetry run
import os
from logging import getLogger
from signal import SIGINT, SIGTERM, SIGABRT, signal

import telegram_mailing_help.db.migration as db
from telegram_mailing_help.appConfig import ApplicationConfiguration
from telegram_mailing_help.db.dao import Dao
from telegram_mailing_help.logic.listPreparation import Preparation
from telegram_mailing_help.telegram import bot
from telegram_mailing_help.web import server

log = getLogger()


class TelegramMailingHelper:

    @staticmethod
    def signal_handler(self, signum, frame) -> None:
        self.telegramBot.stop()
        log.info("Application stopped")
        os._exit(1)

    def __init__(self, appConfig: ApplicationConfiguration):
        log.info("Start the application")
        self.migration = db.Migration(appConfig)
        self.migration.migrate()

        self.dao = Dao(appConfig)

        self.preparation = Preparation(appConfig, self.dao)

        self.telegramBot = bot.MailingBot(appConfig, self.dao, self.preparation)
        self.telegramBot.start()

        self.server = server.BottleServer(appConfig, self.dao, self.preparation)
        self.server.start()

        for sig in (SIGINT, SIGTERM, SIGABRT):
            signal(sig, self.signal_handler)
