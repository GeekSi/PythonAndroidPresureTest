from utils import utils

class CpuInfo:
    usr = 0
    nice = 0
    sys = 0
    idle = 0
    iowait = 0
    irq = 0
    softirq = 0

    def getTotal(self):
        return (self.usr + self.nice + self.sys + self.idle + self.iowait + self.irq + self.softirq)

    def getCpuInfo(self):
        totalCmd="adb shell cat proc/stat"
        totalStat = utils.excuteCmd(totalCmd)
        totalOriArr = totalStat.splitlines()[0].split(' ')
        self.usr = int(totalOriArr[2])
        self.nice = int(totalOriArr[3])
        self.sys = int(totalOriArr[4])
        self.idle = int(totalOriArr[5])
        self.iowait = int(totalOriArr[6])
        self.irq = int(totalOriArr[7])
        self.softirq = int(totalOriArr[8])
