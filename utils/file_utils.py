import os


def writeFileAdd(path, content):
    with open(path, "a") as file:  # 只需要将之前的”w"改为“a"即可，代表追加内容
        file.write(content)


def deleteFile(path):
    if os.path.exists(path) and os.path.isfile(path):
        print("delete file : " + path)
        os.remove(path)


def deleteDir(path):
    if os.path.isdir(path):
        for x in os.listdir(path):
            if os.path.isdir(path + x):
                deleteDir(path + x + "/")
            else:
                deleteFile(path + x)
    else:
        deleteFile(path)


def mkdir(path):
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)


def readFile(path):
    try:
        f = open(path, 'r')
        return f.read()
    finally:
        if f:
            f.close()
