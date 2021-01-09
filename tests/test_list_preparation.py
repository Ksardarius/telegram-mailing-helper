# -*- coding: utf-8 -*-
import logging
import random
import tempfile
import threading
import uuid
from datetime import datetime
from time import sleep

from tests.test_utils import CountDownLatch

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram_mailing_help.db.config import Configuration
from telegram_mailing_help.db.dao import Dao, User, UserState, DispatchListItem
from telegram_mailing_help.db.migration import Migration
from telegram_mailing_help.logic.listPreparation import Preparation
from telegram_mailing_help.telegramMailingHelper import ApplicationConfiguration

log = logging.getLogger()

config = ApplicationConfiguration(
    rootConfigDir='',
    telegramToken='empty',
    db=Configuration(dbFile=tempfile.gettempdir() + "/test_migration_%s.db" % uuid.uuid4()))
m = Migration(config)
m.migrate()

dao = Dao(config)
preparation = Preparation(config, dao)


def test_small_count_of_data():
    dispatch_group_name = "VK bla bla идт ид тп ъъъъопа %s" % uuid.uuid4()
    result = preparation.addDispatchList(
        dispatch_group_name,
        "описание",
        ["only you"],
        10,
        True
    )
    assert result == 1
    assert dao.getDispatchGroupInfo(dispatch_group_name).count == 1


def test_enough_data():
    links_count = 1200
    group_size = 103
    dispatch_group_name = "ОК за свободу прав белых женщин %s" % uuid.uuid4()
    result = preparation.addDispatchList(
        dispatch_group_name,
        "вот какое-то такое описание",
        ["@tralivali_%s" % i for i in range(links_count)],
        group_size,
        False)
    common_count_of_rows = links_count // group_size + (bool(links_count % group_size) * 1)
    assert result == common_count_of_rows
    assert dao.getDispatchGroupInfo(dispatch_group_name).free_count == common_count_of_rows
    assert dispatch_group_name in map(lambda x: x.dispatch_group_name, list(dao.getAllDispatchGroupNames()))


def test_assign_dispatch_lists():
    count_of_disp_list = 100
    count_of_users = 24

    def assign_free_dispatch_list_item(userObj: User, dispatch_group_name: str, counter: CountDownLatch):
        sleep(0.001 * random.randint(1, 50))
        preparation.getAndAssignDispatchList(userObj, dispatch_group_name)
        counter.count_down()

    unique_id = str(uuid.uuid4())
    users = [User(id=None,
                  telegram_id="tid_%s_%s" % (unique_id, i),
                  name="test_name_%s" % i,
                  state=UserState.CONFIRMED.value,
                  created=datetime.now().isoformat())
             for i in range(0, count_of_users)]
    for user in users:
        dao.saveUser(user)

    gr_name = "gr_name_%s" % unique_id

    dispatchLists = [DispatchListItem(id=None,
                                      dispatch_group_name=gr_name,
                                      links_values_butch="links_%s" % i,
                                      description="just description",
                                      is_assigned=False,
                                      created=datetime.now().isoformat())
                     for i in range(0, count_of_disp_list)]
    for item in dispatchLists:
        dao.saveDispatchList(item)

    assert dao.getDispatchGroupInfo(gr_name).count == count_of_disp_list

    counter = CountDownLatch(count_of_disp_list)
    for i in range(0, count_of_disp_list):
        threading.Thread(target=assign_free_dispatch_list_item, args=(users[i % len(users)], gr_name, counter)).start()
    # for i in range(0, count_of_disp_list):
    #     assign_free_dispatch_list_item(users[i % len(users)], gr_name, counter)

    counter.wait(timeout=15)

    dispatchGroupInfo = dao.getDispatchGroupInfo(gr_name)
    assert dispatchGroupInfo.count == count_of_disp_list, "wrong full value of records"
    assert dispatchGroupInfo.free_count == 0, "there is no free butches should be available"
    assert dispatchGroupInfo.assigned_count == count_of_disp_list, "all butches should be assigned"
