from utils import utils
from utils import file_utils
from utils import log_utils

index = 0
java = 0
native = 0
total = 0


def execute(pid, pkgName, filePath):
    cmd = "adb shell dumpsys meminfo %s" % (pid)
    stat = utils.excuteCmd(cmd)

    memArr = stat.splitlines()

    global java
    global native
    global total

    for item in memArr:
        line = item.lstrip()
        if line.startswith("Java Heap:") or line.startswith("Native Heap:") or line.startswith("TOTAL:"):
            valueArr = line.split()
            if valueArr[0] == 'Java':
                java = int(valueArr[2])
            elif valueArr[0] == 'Native':
                native = int(valueArr[2])
            elif valueArr[0] == 'TOTAL:':
                total = int(valueArr[1])

    log_utils.log("%d/java \t %d/native \t %d/total " % (java, native, total))

    memFile = filePath + pkgName + "_mem.txt"
    content = utils.getTime() + "|" + str(int(java/1000)) + "|" + str(int(native/1000)) + "|" + str(int(total/1000))
    file_utils.writeFileAdd(memFile, content + "\n")


def tick(pid, pkgName, filePath):
    global index
    index = index + 1
    if index % 7 == 0:
        execute(pid, pkgName, filePath)
        index = 0
