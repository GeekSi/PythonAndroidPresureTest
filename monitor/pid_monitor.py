from utils import utils
from utils import file_utils
from utils import log_utils

index = 0

def execute(pkgNameArr, filePath):
    for pkgName in pkgNameArr:
        pid = utils.getPid(pkgName)
        if len(pid) == 0:
            log_utils.log("process %s not run" % (pkgName))
        else:
            content = utils.getTime() + "|" + pid + "\n"
            file_utils.writeFileAdd(filePath + pkgName + "_pid.txt", content)


def tick(pkgNameArr, filePath):
    global index
    index = index + 1
    if index % 7 == 0:
        execute(pkgNameArr, filePath)
        index = 0
