from entity import cpu_info
from utils import utils
from utils import file_utils
from utils import log_utils
from monitor import cpudump

index = 0

lastCpuInfo = None

dict = {}


def execute(pkgArr, filePath):
    cpuinfo = cpu_info.CpuInfo()
    cpuinfo.getCpuInfo()

    global lastCpuInfo

    time = utils.getTime()
    global dict

    if lastCpuInfo:
        totalCpu = cpuinfo.getTotal() - lastCpuInfo.getTotal()
        idle = cpuinfo.idle - lastCpuInfo.idle
        usr = cpuinfo.usr - lastCpuInfo.usr
        sys = cpuinfo.sys - lastCpuInfo.sys
        idlePrecent = float(idle * 100) / totalCpu
        usrPrecent = usr * 100 / totalCpu
        sysPrecent = sys * 100 / totalCpu
        usedPrecent = float((totalCpu - idle) * 100) / totalCpu
        log_utils.log("device CPU : \t %d/usr \t %d/sys \t %.1f/idle %.1f/used" % (
            usrPrecent, sysPrecent, idlePrecent, usedPrecent))
        cpuFile = filePath + "device_cpu.txt"
        content = time + "|" + str(int(usedPrecent))
        file_utils.writeFileAdd(cpuFile, content + "\n")
        for pkg in pkgArr:
            if pkg not in dict.keys():
                dict[str(pkg)] = cpudump.cpudump(pkg)
            dict[str(pkg)].dumpCpu(time, totalCpu, filePath)
    else:
        for pkg in pkgArr:
            if pkg not in dict.keys():
                dict[str(pkg)] = cpudump.cpudump(pkg)
            dict[str(pkg)].initData()

    lastCpuInfo = cpuinfo


def tick(pkgArr, filePath):
    global index
    index = index + 1
    if index % 7 == 0:
        execute(pkgArr, filePath)
        index = 0
