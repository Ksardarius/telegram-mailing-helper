# /usr/bin/env poetry run
import json
import os
import sys
from dataclasses import dataclass
from logging import getLogger
from signal import SIGINT, SIGTERM, SIGABRT, signal

import dacite

import telegram_mailing_help.db.config as configDb
import telegram_mailing_help.db.migration as db
import telegram_mailing_help.web.config as configServer
from telegram_mailing_help.db.dao import Dao
from telegram_mailing_help.logic.listPreparation import Preparation
from telegram_mailing_help.telegram import bot
from telegram_mailing_help.web import server

log = getLogger()


@dataclass
class ApplicationConfiguration:
    rootConfigDir: str
    telegramToken: str
    db: configDb.Configuration
    server: configServer.Configuration = configServer.Configuration()


class TelegramMailingHelper:

    @staticmethod
    def _prepareConfig():
        configFile = sys.argv[1] if len(sys.argv) > 1 else "../test_config.json"
        with open(configFile) as json_config:
            appConfig = dacite.from_dict(ApplicationConfiguration, json.load(json_config))
        for key in filter(lambda x: x.startswith('appConfig.'), os.environ.keys()):
            log.info("CONFIGURATION: override value for: %s in appConfig from env", key)
            try:
                exec("%s = %s" % (key, os.environ.get(key)))
            except Exception as e:
                log.warning("Can't apply env variable for config: %s because: %s", key, e)
        return appConfig

    def signal_handler(self, signum, frame) -> None:
        self.telegramBot.stop()
        log.info("Application stopped")
        os._exit(1)

    def __init__(self):
        log.info("Start the application")
        appConfig = self._prepareConfig()
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
