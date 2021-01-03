import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from sqlite3worker import Sqlite3Worker

from telegram_mailing_help.db.utils import getDbFullPath

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger()


class UserState(Enum):
    NEW = 'new'
    CONFIRMED = 'confirmed'
    BLOCKED = 'blocked'

    def getLocalizedMessage(self):
        if self == UserState.NEW:
            return "Новый пользователь"
        elif self == UserState.CONFIRMED:
            return "Подтвержденный"
        elif self == UserState.BLOCKED:
            return "Заблокированный"
        else:
            raise Exception("Unsupported userState: %s" % self.name)


@dataclass
class DispatchListItem:
    id: Optional[int]
    dispatch_group_name: str
    links_values_butch: str
    description: str
    created: str
    is_assigned: bool = False


@dataclass
class User:
    id: Optional[int]
    telegram_id: str
    name: str
    state: str
    created: str


class Dao:
    def __init__(self, config):
        self.config = config
        self.worker = Sqlite3Worker(getDbFullPath(self.config))
        self.dispatchListFields = list(DispatchListItem.__annotations__.keys())
        self.userFields = list(User.__annotations__.keys())

    def freeQuery(self, sql):
        return self.worker.execute(sql)

    def __saveEntity(self, tableName, item):
        if item.id is None:
            sql = "INSERT INTO %(tableName)s (%(fields)s) VALUES (%(values)s)" % {
                "tableName": tableName,
                "fields": ",".join(list(item.__dict__.keys())),
                "values": ",".join(["?"] * len(item.__dict__))
            }
            self.worker.execute(sql, values=tuple(item.__dict__.values()))
            item.id = self.worker.execute("Select last_insert_rowid() as id")[0][0]
        else:
            sql = "UPDATE %(tableName)s set %(values)s where id=?" % {
                "tableName": tableName,
                "values": ",".join(list(map(lambda k: "%s=?" % k, item.__dict__.keys())))
            }
            self.worker.execute(sql, values=tuple(list(item.__dict__.values()) + [item.id]))
        return item

    def saveDispatchList(self, item: DispatchListItem):
        return self.__saveEntity("DISPATCH_LIST", item)

    def saveUser(self, item: User):
        return self.__saveEntity("USERS", item)

    def getDispatchListById(self, id: int):
        result = self.worker.execute("SELECT * from DISPATCH_LIST where id=?", values=(id,))
        if len(result) != 1:
            rez = None
        else:
            rez = DispatchListItem(*result[0])
        return rez

    def getUserById(self, id: int):
        result = self.worker.execute("SELECT * from USERS where id=?", values=(id,))
        if len(result) != 1:
            rez = None
        else:
            rez = User(*result[0])
        return rez

    def confirmUserById(self, id: int):
        self.worker.execute("UPDATE USERS SET state='" + UserState.CONFIRMED.value + "' where id=?", values=(id,))

    def setStateForUserById(self, id: int, state: UserState):
        self.worker.execute("UPDATE USERS SET state='" + state.value + "' where id=?", values=(id,))

    def getUserByTelegramId(self, telegram_id: str):
        result = self.worker.execute("SELECT * from USERS where telegram_id=?", values=(telegram_id,))
        if len(result) != 1:
            rez = None
        else:
            rez = User(*result[0])
        return rez

    def getAllUsers(self):
        result = self.worker.execute("SELECT * from USERS")
        if len(result) == 0:
            return []
        else:
            for row in result:
                yield User(*row)

    def getDispatchListByDispatchGroupName(self, dispatch_group_name: str):
        result = self.worker.execute("SELECT * from DISPATCH_LIST where dispatch_group_name=?",
                                     values=(dispatch_group_name,))
        if len(result) == 0:
            return None
        else:
            for row in result:
                yield DispatchListItem(*row)
