import os
import time
import webbrowser


def excuteCmd(cmd):
    cmd = cmd.replace("\n", "")
    tempFile = os.popen(cmd)
    content = tempFile.read()
    tempFile.close()
    return content


def getTime():
    timeStr = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    return timeStr


def getRootPath():
    return os.getcwd()


def open(url):
    webbrowser.open(url)


def getPid(pkgName):
    return excuteCmd("adb shell pidof " + pkgName).replace("\n", "")
