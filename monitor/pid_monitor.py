from utils import utils
from utils import file_utils

index = 0


def execute(pid, pkgName, filePath):
    content = utils.getTime() + "|" + pid
    file_utils.writeFileAdd(filePath + pkgName + "_pid.txt", content)


def tick(pid, pkgName, filePath):
    global index
    index = index + 1
    if index % 7 == 0:
        execute(pid, pkgName, filePath)
        index = 0
