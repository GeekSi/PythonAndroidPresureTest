from utils import file_utils
from utils import utils
from utils import log_utils
from monitor import cpu_monitor
from monitor import mem_monitor
from monitor import pid_monitor
from monitor import fd_monitor
from monitor import thread_monitor
from threading import Timer
from constant import constants
from controller import uicontroller
from manager import cpu_manager
import create_chars

timeUsed = 0

closeByHandle = False

isRunning = False


def getInfoMation(pkgName):
    if len(pkgName) == 0:
        log_utils.log("请输入要检测的进程名,多个进程用|隔开")
        return
    try:
        log_utils.log("-----------------" + utils.getTime() + "-----------------")
        pkgArr = pkgName.split("|")
        pid_monitor.tick(pkgArr, constants.PATH_PID)
        cpu_monitor.tick(pkgArr, constants.PATH_CPU)
        mem_monitor.tick(pkgArr, constants.PATH_MEM)
        fd_monitor.tick(pkgArr, constants.PATH_FD)
        thread_monitor.tick(pkgArr, constants.PATH_THREAD)
    except Exception as e:
        print(e)
        log_utils.log(str(e))


def close():
    create_chars.createChars()
    utils.open("file://" + constants.PATH_CHARS)


def tick(inc, pkgName, presureTime):
    global closeByHandle
    if closeByHandle:
        uicontroller.setBtnText("开始监控")
        log_utils.log("手动关闭")
        return
    global timeUsed
    timeUsed = timeUsed + 1
    if int(timeUsed) / 60 >= int(presureTime):
        log_utils.log("压测时间到")
        create_chars.createChars()
        utils.open("file://" + constants.PATH_CHARS)
        uicontroller.setBtnText("开始监控")
        cpu_manager.stop()
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
    file_utils.deleteDir(constants.PATH_TEMP)
    file_utils.mkdir(constants.PATH_PID)
    file_utils.mkdir(constants.PATH_MEM)
    file_utils.mkdir(constants.PATH_CPU)
    file_utils.mkdir(constants.PATH_FD)
    file_utils.mkdir(constants.PATH_THREAD)
    file_utils.mkdir(constants.PATH_VIEW)
    file_utils.mkdir(constants.PATH_TASK)
    tick(1, pkgName, presureTime)
    pkgArr = pkgName.split("|")
    cpu_manager.start(pkgArr, constants.PATH_TASK)



def stop():
    global closeByHandle
    closeByHandle = True
    global isRunning
    isRunning = False
    cpu_manager.stop()
    close()
