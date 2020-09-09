from utils import file_utils
from utils import utils
from utils import log_utils
from monitor import cpu_monitor
from monitor import mem_monitor
from monitor import pid_monitor
from threading import Timer
from constant import constants
import create_chars
import webbrowser

timeUsed = 0

closeByHandle = False

isRunning = False


def getInfoMation(pkgName):
    processPid = utils.excuteCmd("adb shell pidof " + pkgName)
    if len(processPid) == 0:
        log_utils.log("process %s not run" % (pkgName))
        return
    try:
        log_utils.log("-----------------" + utils.getTime() + "-----------------")
        pid_monitor.tick(processPid, pkgName, constants.PATH_PID)
        cpu_monitor.tick(processPid, pkgName, constants.PATH_CPU)
        mem_monitor.tick(processPid, pkgName, constants.PATH_MEM)
    except Exception as e:
        log_utils.log(e)


def close():
    create_chars.createChars()
    utils.open("file://" + constants.PATH_CHARS)


def tick(inc, pkgName, presureTime):
    global closeByHandle
    if closeByHandle:
        log_utils.log("手动关闭")
        return
    global timeUsed
    timeUsed = timeUsed + 1
    if int(timeUsed) / 60 >= int(presureTime):
        log_utils.log("压测时间到")
        create_chars.createChars()
        utils.open("file://" + constants.PATH_CHARS)
        return
    getInfoMation(pkgName)
    t = Timer(inc, tick, (inc, pkgName, presureTime))
    t.daemon = True
    t.start()


def start(pkgName, presureTime):
    global isRunning
    global closeByHandle
    closeByHandle = False
    isRunning = True
    file_utils.deleteDir(constants.PATH_PID)
    file_utils.deleteDir(constants.PATH_MEM)
    file_utils.deleteDir(constants.PATH_CPU)
    file_utils.deleteDir(constants.PATH_VIEW)
    file_utils.mkdir(constants.PATH_PID)
    file_utils.mkdir(constants.PATH_MEM)
    file_utils.mkdir(constants.PATH_CPU)
    file_utils.mkdir(constants.PATH_VIEW)
    tick(1, pkgName, presureTime)


def stop():
    global closeByHandle
    closeByHandle = True
    global isRunning
    isRunning = False
    close()
