import json
import os
import sys
from dataclasses import dataclass

import dacite

import telegram_mailing_help.db.config as configDb
import telegram_mailing_help.web.config as configServer


@dataclass
class ApplicationConfiguration:
    rootConfigDir: str
    telegramToken: str
    logFileName: str
    db: configDb.Configuration
    server: configServer.Configuration = configServer.Configuration()


def prepareConfig():
    configFile = sys.argv[1] if len(sys.argv) > 1 else "../test_config.json"
    with open(configFile) as json_config:
        appConfig = dacite.from_dict(ApplicationConfiguration, json.load(json_config))
    for key in filter(lambda x: x.startswith('appConfig.'), os.environ.keys()):
        print("CONFIGURATION: override value for: %s in appConfig from env" % key)
        try:
            exec("%s = %s" % (key, os.environ.get(key)))
        except Exception as e:
            print("Can't apply env variable for config: %s because: %s" % (key, e))
    return appConfig
