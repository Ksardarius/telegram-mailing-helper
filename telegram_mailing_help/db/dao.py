import hashlib
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlite3worker import Sqlite3Worker

from telegram_mailing_help.db.daoExp import OptimisticLockException
from telegram_mailing_help.db.utils import getDbFullPath

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger()


class AssignState(Enum):
    ASSIGNED = 'assigned'
    ROLLBACK = 'rollback'


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
    enabled: bool = True
    _check_sum: str = None
    _version: int = 0
    is_assigned: bool = False


@dataclass
class DispatchGroupInfo:
    dispatch_group_name: str
    count: int
    assigned_count: int
    free_count: int
    enabled: bool


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

    def __saveEntity(self, tableName, item, useVersion=False):
        if item.id is None:
            if useVersion:
                item._version = 0
            sql = "INSERT INTO %(tableName)s (%(fields)s) VALUES (%(values)s)" % {
                "tableName": tableName,
                "fields": ",".join(list(item.__dict__.keys())),
                "values": ",".join(["?"] * len(item.__dict__))
            }
            self.worker.execute(sql, values=tuple(item.__dict__.values()))
            item.id = self.worker.execute("Select last_insert_rowid() as id")[0][0]
        else:
            setVersionWhere = ""
            if useVersion:
                setVersionWhere = "and _version=%s" % item._version
                item._version = item._version + 1
            sql = "UPDATE %(tableName)s set %(values)s where id=? %(setVersionWhere)s" % {
                "tableName": tableName,
                "values": ",".join(list(map(lambda k: "%s=?" % k, item.__dict__.keys()))),
                "setVersionWhere": setVersionWhere
            }
            self.worker.execute(sql, values=tuple(list(item.__dict__.values()) + [item.id]))
            if useVersion:
                if self.worker.execute(
                        "SELECT COUNT(id) FROM %(tableName)s WHERE id=? AND _version=?" % {"tableName": tableName},
                        values=(item.id, item._version))[0][0] != 1:
                    raise OptimisticLockException()
        return item

    def getFreeDispatchListItem(self, dispatch_group_name):
        result = self.worker.execute(
            "SELECT * from DISPATCH_LIST WHERE dispatch_group_name=? AND is_assigned=0 LIMIT 1",
            values=(dispatch_group_name,))
        if len(result) != 1:
            return None
        else:
            return DispatchListItem(*result[0])

    def assignBlockIntoUser(self, user: User, dispatch_list: DispatchListItem):
        self.worker.execute("UPDATE DISPATCH_LIST set is_assigned=1, _version=? WHERE id=? and _version=?",
                            values=(dispatch_list._version + 1, dispatch_list.id, dispatch_list._version))
        assignId = str(uuid.uuid4())
        self.worker.execute(
            "INSERT INTO DISPATCH_LIST_ASSIGNS (uuid,dispatch_list_id,users_id,state,change_date) values (?,?,?,?,?)",
            values=(assignId, dispatch_list.id, user.id, AssignState.ASSIGNED.value, datetime.now().isoformat()))
        if self.worker.execute(
                "SELECT COUNT(dl.id) FROM DISPATCH_LIST dl LEFT JOIN DISPATCH_LIST_ASSIGNS dla ON (dla.dispatch_list_id=dl.id ) "
                "WHERE dl.id =? AND dl._version=? AND dla.users_id =?",
                values=(dispatch_list.id, dispatch_list._version + 1, user.id))[0][0] != 1:
            self.worker.execute("DELETE FROM DISPATCH_LIST_ASSIGNS WHERE uuid=?",
                                values=(assignId,))
            raise OptimisticLockException()
        else:
            dispatch_list._version = dispatch_list._version + 1
            dispatch_list.is_assigned = True

    def saveDispatchList(self, item: DispatchListItem):
        item._check_sum = hashlib.md5(
            bytearray(item.links_values_butch + item.dispatch_group_name, encoding="utf-8")).hexdigest()
        return self.__saveEntity("DISPATCH_LIST", item, useVersion=True)

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

    def getAllDispatchGroupNames(self):
        result = self.worker.execute("SELECT DISTINCT(dispatch_group_name) from DISPATCH_LIST")
        if len(result) == 0:
            return []
        else:
            for row in result:
                yield row[0]

    def getEnabledDispatchGroupNames(self):
        result = self.worker.execute("SELECT DISTINCT(dispatch_group_name) from DISPATCH_LIST WHERE enabled = 1")
        if len(result) == 0:
            return []
        else:
            for row in result:
                yield row[0]

    def enableDispatchGroupName(self, dispatch_group_name):
        self.worker.execute("UPDATE DISPATCH_LIST SET enabled=1,_version=_version+1 WHERE dispatch_group_name=?",
                            values=(dispatch_group_name,))

    def disableDispatchGroupName(self, dispatch_group_name):
        self.worker.execute("UPDATE DISPATCH_LIST SET enabled=0,_version=_version+1 WHERE dispatch_group_name=?",
                            values=(dispatch_group_name,))

    def getDispatchGroupInfo(self, dispatch_group_name):
        result = self.worker.execute(
            "SELECT dispatch_group_name,COUNT(id),SUM(is_assigned),enabled FROM DISPATCH_LIST WHERE dispatch_group_name=? GROUP BY dispatch_group_name",
            values=(dispatch_group_name,))
        if len(result) == 0:
            return None
        else:
            row = result[0]
            return DispatchGroupInfo(
                dispatch_group_name=row[0],
                count=row[1],
                assigned_count=row[2],
                free_count=row[1] - row[2],
                enabled=bool(row[3])
            )
