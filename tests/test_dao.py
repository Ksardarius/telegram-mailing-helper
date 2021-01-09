import logging
import tempfile
import threading
import uuid
from datetime import datetime

from telegram_mailing_help.db.config import Configuration
from telegram_mailing_help.db.dao import Dao, UserState, DispatchGroupInfo
from telegram_mailing_help.db.dao import DispatchListItem
from telegram_mailing_help.db.dao import User
from telegram_mailing_help.db.migration import Migration
from telegram_mailing_help.appConfig import ApplicationConfiguration
from tests.test_utils import CountDownLatch

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger()

config = ApplicationConfiguration(
    rootConfigDir='',
    telegramToken='empty',
    logFileName='/tmp/log.log',
    db=Configuration(dbFile=tempfile.gettempdir() + "/test_migration_%s.db" % uuid.uuid4()))
m = Migration(config)
m.migrate()

dao = Dao(config)


def test_save_dispatch_list_item():
    item = DispatchListItem(
        id=None,
        dispatch_group_name="OK",
        links_values_butch="l1\nl3",
        description="test_data",
        created=datetime.now().isoformat())
    item = dao.saveDispatchList(item)
    assert item.id != 0
    rezFromDaoById = dao.getDispatchListById(item.id)
    assert item == rezFromDaoById

    item = DispatchListItem(
        id=None,
        dispatch_group_name="OK",
        links_values_butch="l1\nl2",
        description="test_data",
        created=datetime.now().isoformat())
    item = dao.saveDispatchList(item)
    rezFromDaoById = dao.getDispatchListById(item.id)
    assert item == rezFromDaoById
    assert len(list(dao.getDispatchListByDispatchGroupName(item.dispatch_group_name))) == 2

    item.description = "new_description"
    currentId = item.id
    item = dao.saveDispatchList(item)
    rezFromDaoById = dao.getDispatchListById(currentId)
    assert rezFromDaoById.description == "new_description"
    assert item.id == currentId
    assert rezFromDaoById.id == currentId


def test_get_dispatch_groups():
    dao.freeQuery("delete from DISPATCH_LIST;")
    item1 = DispatchListItem(
        id=None,
        dispatch_group_name="gr1",
        links_values_butch="l1\nl2",
        description="test_data",
        created=datetime.now().isoformat())
    item2 = DispatchListItem(
        id=None,
        dispatch_group_name="gr1",
        links_values_butch="l3\nl4",
        description="test_data",
        created=datetime.now().isoformat())
    item3 = DispatchListItem(
        id=None,
        dispatch_group_name="gr2",
        links_values_butch="l5\nl6",
        description="test_data",
        created=datetime.now().isoformat())
    for item in [item1, item2, item3]:
        dao.saveDispatchList(item)

    assert dao.freeQuery("select count(*) from DISPATCH_LIST")[0][0] == 3
    assert sorted(map(lambda x: x.dispatch_group_name, list(dao.getAllDispatchGroupNames()))) == ["gr1", "gr2"]


def test_get_info_about_dispatch_group():
    gr_name = "test_gr_name_%s" % uuid.uuid4()

    item1 = DispatchListItem(
        id=None,
        dispatch_group_name=gr_name,
        links_values_butch="l1\nl2\n%s" % uuid.uuid4(),
        description="test_data",
        created=datetime.now().isoformat(),
        is_assigned=True)
    item2 = DispatchListItem(
        id=None,
        dispatch_group_name=gr_name,
        links_values_butch="l1\nl2\n%s" % uuid.uuid4(),
        description="test_data",
        created=datetime.now().isoformat())
    item3 = DispatchListItem(
        id=None,
        dispatch_group_name=gr_name,
        links_values_butch="l1\nl2\n%s" % uuid.uuid4(),
        description="test_data",
        created=datetime.now().isoformat())
    for item in [item1, item2, item3]:
        dao.saveDispatchList(item)
    assert dao.getDispatchGroupInfo(gr_name) == DispatchGroupInfo(dispatch_group_name=gr_name, description="test_data",
                                                                  count=3, assigned_count=1, free_count=2, enabled=True)
    assert dao.getDispatchGroupInfo(gr_name + "_failed") is None


def multi_thread(index, counter, net_name):
    item = DispatchListItem(
        id=None,
        dispatch_group_name=net_name,
        links_values_butch="l1\nl2\nuser_%s" % uuid.uuid4(),
        description="test_data_%s" % index,
        created=datetime.now().isoformat())
    log.info("test_net_id: %s", dao.saveDispatchList(item).id)
    counter.count_down()


def test_multi_threading_add_dispatch_list():
    net_name = "test_net_%s" % uuid.uuid4()
    attempts = 100
    counter = CountDownLatch(attempts)
    for i in range(attempts):
        threading.Thread(target=multi_thread, args=(i, counter, net_name)).start()

    counter.wait(timeout=5)
    rez = list(dao.getDispatchListByDispatchGroupName(net_name))
    assert len(rez) == attempts, "wrong records count, should be %s" % attempts


def test_save_user():
    user = User(
        id=None,
        telegram_id="tel_id_333",
        name="telegram_name",
        state=UserState.NEW.value,
        created=datetime.now().isoformat()
    )
    user = dao.saveUser(user)
    assert user.id is not None, "User id should be set after save"
    userFromBaseById = dao.getUserById(user.id)
    userFromBaseByTelegramId = dao.getUserByTelegramId(user.telegram_id)
    assert user == userFromBaseById
    assert user == userFromBaseByTelegramId


def test_user_telegram_id_unique_index():
    test_user_name = "name_%s" % uuid.uuid4()
    user1 = User(
        id=None,
        telegram_id="tel_id_1",
        name=test_user_name,
        state=UserState.NEW.value,
        created=datetime.now().isoformat()
    )
    user2 = User(
        id=None,
        telegram_id="tel_id_2",
        name=test_user_name,
        state=UserState.NEW.value,
        created=datetime.now().isoformat()
    )
    user1 = dao.saveUser(user1)
    user2 = dao.saveUser(user2)
    testUsersCount = dao.freeQuery("select count(*) from users where name='%s'" % test_user_name)[0][0]
    assert testUsersCount == 2
    assert user1.id is not None
    assert user2.id is not None
