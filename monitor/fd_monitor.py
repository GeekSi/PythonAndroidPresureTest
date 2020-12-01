from utils import utils
from utils import file_utils
from utils import log_utils

index = 0


def execute(pkgArr, filePath):
    time = utils.getTime()

    log_utils.log("------------catch fdcount------------")
    for pkg in pkgArr:
        pid = utils.getPid(pkg)
        fdCommand = 'adb shell ls proc/' + pid + '/fd | wc -l'
        fdCount = utils.excuteCmd(fdCommand)
        content = time + "|" + fdCount
        fdPath = filePath + pkg + "_fd.txt"
        file_utils.writeFileAdd(fdPath, content)


def tick(pkgArr, filePath):
    global index
    index = index + 1
    if index % 60 == 0:
        execute(pkgArr, filePath)
        index = 0
