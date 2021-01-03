import json
import logging
import pathlib
import threading
from functools import wraps

from bottle import Bottle, request, response, get, post, template, static_file, run as run_bottle

from telegram_mailing_help import __version__
from telegram_mailing_help.db.dao import Dao, UserState

log = logging.getLogger("bottleServer")

db: Dao = None


def _getTemplateFile(templateName):
    return str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + templateName


@get("/info")
def info():
    return {"version": __version__, "app": "telegram_mailing_helper"}


@get("/pages/users.html")
def users():
    return template(_getTemplateFile("users.tpl"), users=db.getAllUsers(), userStateCls=UserState)


@get("/pages/<page>")
def pages(page):
    return static_file(page, root=_getTemplateFile(""))


@post("/api/users/confirm")
def confirmUser():
    body = json.load(request.body)
    db.setStateForUserById(body["id"], UserState.CONFIRMED)
    return {"success": True}


@post("/api/users/block")
def confirmUser():
    body = json.load(request.body)
    db.setStateForUserById(body["id"], UserState.BLOCKED)
    return {"success": True}


class BottleServer(threading.Thread):

    def __init__(self, config, dao: Dao):
        global db
        threading.Thread.__init__(self, name=__name__)
        db = dao
        self.daemon = True
        self.config = config
        # Event to start the exit process.
        self._exit_event = threading.Event()
        # Event that closes out the threads.
        self._close_lock = threading.Lock()

    def logToLogger(self, fn):
        @wraps(fn)
        def _logToLogger(*args, **kwargs):
            actual_response = fn(*args, **kwargs)
            log.info('%s %s %s %s' % (request.remote_addr,
                                      request.method,
                                      request.url,
                                      response.status))
            return actual_response

        return _logToLogger

    def run(self) -> None:
        server = Bottle()
        server.install(self.logToLogger)
        run_bottle(host=self.config.server.host,
                   port=self.config.server.port,
                   server=self.config.server.engine,
                   plugins=[self.logToLogger],
                   quiet=True)
