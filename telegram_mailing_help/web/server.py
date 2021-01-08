import json
import logging
import pathlib
import threading
from functools import wraps

from bottle import BaseRequest, Bottle, request, response, get, post, redirect, template, static_file, run as run_bottle

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 1024 * 10

from telegram_mailing_help import __version__
from telegram_mailing_help import use_gevent
from telegram_mailing_help.db.dao import Dao, UserState
from telegram_mailing_help.logic.listPreparation import Preparation

log = logging.getLogger("bottleServer")

db: Dao = None
preparation: Preparation = None


def _getTemplateFile(templateName):
    return str(pathlib.Path(__file__).parent.absolute()) + '/templates/' + templateName


@get("/")
def rootRedirect():
    return redirect("/pages/dispatch_lists.html")


@get("/info")
def info():
    return {"version": __version__, "app": "telegram_mailing_helper"}


@get("/pages/users.html")
def users():
    return template(_getTemplateFile("users.tpl"), users=db.getAllUsers(), userStateCls=UserState)


@get("/pages/dispatch_lists.html")
def users():
    return template(_getTemplateFile("dispatch_lists.tpl"), dispatchGroupNames=list(db.getAllDispatchGroupNames()))


@get("/pages/<page>")
def pages(page):
    return static_file(page, root=_getTemplateFile(""))


@post("/api/lists/add")
def addDispatchList():
    dispatchGroupName = request.forms.name
    description = request.forms.description
    links = request.forms.list.splitlines()
    groupSize = int(request.forms.groupSize)
    disableByDefault = bool(request.forms.disableByDefault)
    countOfAddedDispatchList = preparation.addDispatchList(dispatchGroupName, description, links, groupSize,
                                                           disableByDefault)
    return {"success": True, "countOfAddedItems": countOfAddedDispatchList}


@get("/api/lists/<gr_name>")
def getDispatchGroupInfo(gr_name):
    info = db.getDispatchGroupInfo(gr_name)
    return template(_getTemplateFile("dispatch_group_info.tpl"), data={
        "info": info,
        "state": {
            "text": "Скрыть кнопку" if info.enabled else "Показывать кнопку",
            "value": "disable" if info.enabled else "enable"
        }
    })


@post("/api/lists/<gr_name>/state")
def changeStateOfGroupAt(gr_name):
    body = json.load(request.body)
    if body["state"] == "enable":
        db.enableDispatchGroupName(gr_name)
    elif body["state"] == "disable":
        db.disableDispatchGroupName(gr_name)
    else:
        raise RuntimeError("Unknown state for group: %s : %s" % (gr_name, body["state"]))
    return {"success": True, "gr_name": gr_name}


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

    def __init__(self, config, dao: Dao, preparationList: Preparation):
        global db, preparation
        threading.Thread.__init__(self, name=__name__)
        db = dao
        preparation = preparationList
        self.daemon = True
        self.config = config
        # Event to start the exit process.
        self._exit_event = threading.Event()
        # Event that closes out the threads.
        self._close_lock = threading.Lock()

    def logToLogger(self, fn):
        @wraps(fn)
        def _logToLogger(*args, **kwargs):
            try:
                actual_response = fn(*args, **kwargs)
                log.info('%s %s %s %s',
                         request.remote_addr,
                         request.method,
                         request.url,
                         response.status)
                return actual_response
            except Exception as e:
                log.exception("Exception while call %s %s %s %s:",
                              request.remote_addr,
                              request.method,
                              request.url,
                              response.status)
                raise e

        return _logToLogger

    def run(self) -> None:
        server = Bottle()
        server.install(self.logToLogger)
        run_bottle(host=self.config.server.host,
                   port=self.config.server.port,
                   server="gevent" if use_gevent else "wsgiref",
                   plugins=[self.logToLogger],
                   quiet=True)
