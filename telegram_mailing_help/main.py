use_gevent = False
if use_gevent:
    from gevent import monkey
    monkey.patch_all()

import logging
from time import sleep

from telegramMailingHelper import TelegramMailingHelper

log = logging.getLogger()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
if __name__ == '__main__':
    TelegramMailingHelper()
    sleep(3600)
