import pathlib
from logging import getLogger

from yoyo import get_backend
from yoyo import read_migrations

from telegram_mailing_help.db.utils import getDbFullPath

log = getLogger("migration")


class Migration:
    def __init__(self, config):
        self.migrations = read_migrations(str(pathlib.Path(__file__).parent.absolute()) + '/migration')
        self.backend = get_backend("sqlite:///" + getDbFullPath(config))

    def migrate(self):
        log.info("Start migration...")
        with self.backend.lock():
            # Apply any outstanding migrations
            self.backend.apply_migrations(self.backend.to_apply(self.migrations))
        log.info("Migration: success!")

    def rollback(self):
        with self.backend.lock():
            # Rollback all migrations
            self.backend.rollback_migrations(self.backend.to_rollback(self.migrations))
