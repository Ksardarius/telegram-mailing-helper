from telegram_mailing_help import use_gevent
if use_gevent:
    from gevent import monkey

    monkey.patch_all()

import logging
import systemd.daemon

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')
from time import sleep
from telegramMailingHelper import TelegramMailingHelper

log = logging.getLogger()

if __name__ == '__main__':
    log.info('Starting up ...')
    TelegramMailingHelper()
    log.info('Startup complete')
    systemd.daemon.notify(systemd.daemon.Notification.READY)
    while True:
        sleep(100)
