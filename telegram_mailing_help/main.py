from telegram_mailing_help.appConfig import prepareConfig

config = prepareConfig()
if config.server.engine == "gevent":
    from gevent import monkey

    monkey.patch_all()

import logging
from logging.handlers import RotatingFileHandler
import systemd.daemon

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s',
                    handlers=[logging.StreamHandler(),
                              RotatingFileHandler(
                                  backupCount=100,
                                  maxBytes=1024 * 1024 * 10,
                                  filename=config.logFileName
                                  if config.logFileName.startswith("/") else
                                  config.rootConfigDir + "/" + config.logFileName)])
from time import sleep
from telegramMailingHelper import TelegramMailingHelper

log = logging.getLogger()

if __name__ == '__main__':
    log.info('Starting up ...')
    TelegramMailingHelper(config)
    log.info('Startup complete')
    systemd.daemon.notify(systemd.daemon.Notification.READY)
    while True:
        sleep(100)
