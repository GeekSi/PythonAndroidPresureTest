from utils import utils
from utils import file_utils
from utils import log_utils

index = 0


def execute(pkgArr, filePath):
    time = utils.getTime()
    log_utils.log("------------catch threadcount------------")

    for pkg in pkgArr:
        pid = utils.getPid(pkg)
        threadCommand = 'adb shell ls proc/' + pid + '/task | wc -l'
        threadCount = utils.excuteCmd(threadCommand)
        content = time + "|" + threadCount
        fdPath = filePath + pkg + "_thread.txt"
        file_utils.writeFileAdd(fdPath, content)


def tick(pkgArr, filePath):
    global index
    index = index + 1
    if index % 60 == 0:
        execute(pkgArr, filePath)
        index = 0
