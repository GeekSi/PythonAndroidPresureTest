from controller import uicontroller


def log(msg):
    print(msg)
    uicontroller.appendText(msg)
