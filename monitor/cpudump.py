from utils import utils
from utils import log_utils
from utils import file_utils
from entity import cpu_info_process


class cpudump:
    pid = 0
    pkgName = ''
    lastProcessCpuInfo = None

    def __init__(self, pkgName):
        self.pkgName = pkgName

    def dumpCpu(self, time, totalCpu, filePath):
        pid = utils.getPid(self.pkgName)
        if self.pid != 0 and pid != 0 and self.pid != pid:
            # pid有变化,需要清空上一次的的取值,从新取值
            self.lastProcessCpuInfo = None
            cpuProcessInfo = cpu_info_process.CpuProcessInfo()
            cpuProcessInfo.getCpuInfo(pid)
            self.lastProcessCpuInfo = cpuProcessInfo
            self.pid = pid
            return

        cpuProcessInfo = cpu_info_process.CpuProcessInfo()
        cpuProcessInfo.getCpuInfo(pid)
        if self.lastProcessCpuInfo:
            processTotal = cpuProcessInfo.getTotal() - self.lastProcessCpuInfo.getTotal()
            processPrecent = processTotal * 100 / totalCpu
            log_utils.log(self.pkgName + " CPU : %d " % (processPrecent))
            cpuFile = filePath + self.pkgName + "_cpu.txt"
            content = time + "|" + str(int(processPrecent))
            file_utils.writeFileAdd(cpuFile, content + "\n")
        self.lastProcessCpuInfo = cpuProcessInfo

    def initData(self):
        self.pid = utils.getPid(self.pkgName)
        cpuProcessInfo = cpu_info_process.CpuProcessInfo()
        cpuProcessInfo.getCpuInfo(self.pid)
        self.lastProcessCpuInfo = cpuProcessInfo
