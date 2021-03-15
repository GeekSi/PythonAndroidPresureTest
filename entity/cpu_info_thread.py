from utils import utils


class CpuThreadsInfo:
    utime = 0
    stime = 0
    cutime = 0
    cstime = 0
    threadName = ""
    threadId = 0
    threadStatus = ""
    total = 0

    def getTotal(self):
        if self.total == 0:
            self.total = (self.utime + self.stime)
        return self.total

    def parseThreadData(self, statStr):
        # processCmd="adb shell cat proc/%s/stat"%(pid).replace("\n","")
        # processStat = utils.excuteCmd(processCmd)
        # '1016 (glide-disk-cach'
        # S 286 286 0 0 -1 1077952576 2671 4372 4 0 90 10 237 176 29 9 141 0 1713 1559412736 48766 4294967295 2342060032 2342080057 3204208960 2322968552 2886413528 0 4612 4096 1073775868 1 0 0 -1 3 0 0 0 0 0 2342087856 2342088704 2368909312 3204209231 3204209307 3204209307 3204210660 0
        processCpuInfo = statStr.split(') ')
        processInfoArr = str(processCpuInfo[0]).split(' (')
        self.threadId = processInfoArr[0]
        self.threadName = processInfoArr[1]
        processOriArr = processCpuInfo[1].split(' ')

        self.threadStatus = processOriArr[0]

        self.utime = int(processOriArr[11])
        self.stime = int(processOriArr[12])
        self.cutime = int(processOriArr[13])
        self.cstime = int(processOriArr[14])
