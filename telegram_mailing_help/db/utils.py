from datetime import datetime

def getDbFullPath(config):
    if config.db.dbFile.startswith("/"):
        fullDbFile = config.db.dbFile
    else:
        fullDbFile = config.rootConfigDir + "/" + config.db.dbFile
    return fullDbFile


def dictFactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def isoDatetimeStringToDatetime(isoDatetimeString: str):
    return datetime.strptime(isoDatetimeString)

