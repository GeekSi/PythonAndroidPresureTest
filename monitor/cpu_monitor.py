from entity import cpu_info
from entity import cpu_info_process
from utils import utils
from utils import file_utils
from utils import log_utils

index = 0

lastCpuInfo = None

lastProcessCpuInfo = None

currentPid = 0


def execute(pid, pkgName, filePath):
    cpuinfo = cpu_info.CpuInfo()
    cpuinfo.getCpuInfo()

    cpuProcessInfo = cpu_info_process.CpuProcessInfo()
    cpuProcessInfo.getCpuInfo(pid)

    global lastCpuInfo
    global lastProcessCpuInfo

    if lastCpuInfo and lastProcessCpuInfo:
        totalCpu = cpuinfo.getTotal() - lastCpuInfo.getTotal()
        idle = cpuinfo.idle - lastCpuInfo.idle
        usr = cpuinfo.usr - lastCpuInfo.usr
        sys = cpuinfo.sys - lastCpuInfo.sys
        processTotal = cpuProcessInfo.getTotal() - lastProcessCpuInfo.getTotal()
        processPrecent = processTotal * 100 / totalCpu
        idlePrecent = float(idle * 100) / totalCpu
        usrPrecent = usr * 100 / totalCpu
        sysPrecent = sys * 100 / totalCpu
        usedPrecent = float((totalCpu - idle) * 100) / totalCpu
        log_utils.log("process CPU : %d " % (processPrecent))
        log_utils.log("device CPU : \t %d/usr \t %d/sys \t %.1f/idle %.1f/used" % (
            usrPrecent, sysPrecent, idlePrecent, usedPrecent))
        cpuFile = filePath + pkgName + "_cpu.txt"
        content = utils.getTime() + "|" + str(int(processPrecent)) + "|" + str(int(usedPrecent))
        file_utils.writeFileAdd(cpuFile, content + "\n")

    lastCpuInfo = cpuinfo
    lastProcessCpuInfo = cpuProcessInfo


def tick(pid, pkgName, filePath):
    global currentPid
    global lastCpuInfo
    global lastProcessCpuInfo

    if currentPid != 0 and currentPid != pid:
        # pid有变化,需要清除缓存数据
        lastCpuInfo = None
        lastProcessCpuInfo = None
        currentPid = 0

    if currentPid == 0:
        execute(pid, pkgName, filePath)
        currentPid = pid

    global index
    index = index + 1
    if index % 7 == 0:
        execute(pid, pkgName, filePath)
        index = 0
