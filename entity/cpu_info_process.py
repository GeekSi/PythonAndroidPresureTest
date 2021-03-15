from utils import utils


class CpuProcessInfo:
    utime = 0
    stime = 0
    cutime = 0
    cstime = 0

    def getTotal(self):
        return (self.utime + self.stime)

    def getCpuInfo(self, pid):
        processCmd = "adb shell cat proc/%s/stat" % (pid).replace("\n", "")
        processStat = utils.excuteCmd(processCmd)
        processOriArr = processStat.split(' ')

        self.utime = int(processOriArr[13])
        self.stime = int(processOriArr[14])
        self.cutime = int(processOriArr[15])
        self.cstime = int(processOriArr[16])
