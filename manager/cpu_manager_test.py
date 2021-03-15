from entity import cpu_info_process
from entity import cpu_info_thread
from utils import log_utils
from utils import utils


def getProcessAndTaskInfo(pkg):
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
        log_utils.log(
            "%s\t[%s][%s]\tused cpu \t%.2f %% \t\t%s" % (
                item.threadName.ljust(20), str(item.threadId).ljust(4), item.threadStatus, (item.getTotal() * 100 / cpuProcessInfo.getTotal()),
                item.getTotal()))

    log_utils.log("tasksTotal / processTotal : %.5f" % (tasksTotal / cpuProcessInfo.getTotal()))

    log_utils.log("cout %d : taskTotal %d processTotal %d" % (len(threadCpuArr), tasksTotal, cpuProcessInfo.getTotal()))


# getProcessAndTaskInfo("com.example.statusbartest")
# getProcessAndTaskInfo("com.baidu.launcher")
getProcessAndTaskInfo("com.tencent.qqlive.audiobox")
