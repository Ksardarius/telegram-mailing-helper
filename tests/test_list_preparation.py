# -*- coding: utf-8 -*-
import logging
import tempfile
import uuid

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram_mailing_help.db.config import Configuration
from telegram_mailing_help.db.dao import Dao
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
    assert dispatch_group_name in list(dao.getAllDispatchGroupNames())
