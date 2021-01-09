# /usr/bin/env poetry run
import sys
from logging import getLogger
from signal import SIGINT, SIGTERM, SIGABRT, signal
from time import sleep

import systemd.daemon

import telegram_mailing_help.db.migration as db
from telegram_mailing_help.appConfig import ApplicationConfiguration
from telegram_mailing_help.db.dao import Dao
from telegram_mailing_help.logic.listPreparation import Preparation
from telegram_mailing_help.telegram import bot
from telegram_mailing_help.web import server

log = getLogger()


class TelegramMailingHelper:

    def signal_handler(self, signum, frame) -> None:

        while True:
            try:
                self.telegramBot.stop()
                break
            except Exception:
                log.exception("Exception while stop telegram bot")
            log.info("Sleep 1 second...")
            sleep(1)
        log.info("Application stopped")
        systemd.daemon.notify(systemd.daemon.Notification.STOPPING)
        sys.exit()

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
