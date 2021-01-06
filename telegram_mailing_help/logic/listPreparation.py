import logging
import threading
from datetime import datetime

from telegram_mailing_help.db.dao import Dao, DispatchListItem, User
from telegram_mailing_help.db.daoExp import OptimisticLockException

log = logging.getLogger("helperLogic")


class Preparation:
    def __init__(self, config, dao: Dao):
        self.dao = dao
        self.config = config
        self._assignLock = threading.Lock()

    @staticmethod
    def _chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def addDispatchList(self, dispatch_group_name: str, description: str, links: list, devideBy: int,
                        disableByDefault: bool):
        countOfAdded = 0
        dispatchTemplate = DispatchListItem(
            id=None,
            dispatch_group_name=dispatch_group_name,
            links_values_butch=None,
            description=description,
            is_assigned=False,
            enabled=not disableByDefault,
            created=datetime.now().isoformat()
        )
        for chunk in self._chunks(links, devideBy):
            dispatchTemplate.id = None
            dispatchTemplate.links_values_butch = "\n".join(chunk)
            self.dao.saveDispatchList(dispatchTemplate)
            countOfAdded += 1
        return countOfAdded

    def getAndAssignDispatchList(self, user: User, dispatch_group_name: str):
        with self._assignLock:
            attempt = 1
            item = None
            while attempt < 5:
                try:
                    item = self.dao.getFreeDispatchListItem(dispatch_group_name)
                    if item:
                        self.dao.assignBlockIntoUser(user, item)
                    break
                except OptimisticLockException:
                    log.warning("Can't assign dispatchList with id: %s optimistic lock, attempt: %s", item.id, attempt)
                    item = None
                attempt += 1

            if item:
                return item.links_values_butch
            else:
                return "Свободных блоков для данного списка больше нет," \
                       " пожалуйста обратитесь к куратору для их добавления или для скрытия данного списка"
