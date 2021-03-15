from entity import cpu_info
from entity import cpu_info_process
from entity import cpu_info_thread
from utils import log_utils
from utils import utils
from utils import file_utils
from monitor import cpudump

startDeviceCpuInfo = None
pkgArr = []

dict = {}

taskPath = ""


def start(pkgArrValue, taskPathValue):
    log_utils.log("cpu_manager start")
    global pkgArr
    global startDeviceCpuInfo
    global dict
    global taskPath

    taskPath = taskPathValue

    pkgArr = pkgArrValue


def stop():
    log_utils.log("cpu_manager stop")
    global startDeviceCpuInfo
    global pkgArr

    for pkg in pkgArr:
        getProcessAndTaskInfo(pkg)


def getProcessAndTaskInfo(pkg):
    global taskPath
    filePath = taskPath + "/" + pkg + "_task.txt"
    cpuProcessInfo = cpu_info_process.CpuProcessInfo()
    pid = utils.getPid(pkg)
    log_utils.log(pid)
    cmd = "adb shell cat proc/%s/task/*/stat" % (pid).replace("\n", "")
    content = utils.excuteCmd(cmd)
    cpuProcessInfo.getCpuInfo(pid)
    taskCpuLineArr = content.splitlines()
    tasksTotal = 0
    threadCpuArr = []
    for i in range(len(taskCpuLineArr)):
        threadCpuInfo = cpu_info_thread.CpuThreadsInfo()
        threadCpuInfo.parseThreadData(taskCpuLineArr[i])
        tasksTotal = tasksTotal + threadCpuInfo.getTotal()
        threadCpuArr.append(threadCpuInfo)

    threadCpuArr = sorted(threadCpuArr, key=lambda x: x.total, reverse=True)
    for i in range(len(threadCpuArr)):
        item = threadCpuArr[i]

        content = "%s\t[%s][%s]\tused cpu \t%.2f %% \t\t%s\n" % (
            item.threadName.ljust(20), str(item.threadId).ljust(4), item.threadStatus,
            (item.getTotal() * 100 / cpuProcessInfo.getTotal()), item.getTotal())

        file_utils.writeFileAdd(filePath, content)

        log_utils.log(content)
    tempContent = "tasksTotal / processTotal : %.5f\n" % (tasksTotal / cpuProcessInfo.getTotal())
    file_utils.writeFileAdd(filePath, tempContent)
    log_utils.log(tempContent)
    tempContent = "cout %d : taskTotal %d processTotal %d\n" % (len(threadCpuArr), tasksTotal, cpuProcessInfo.getTotal())
    file_utils.writeFileAdd(filePath, tempContent)
    log_utils.log(tempContent)
