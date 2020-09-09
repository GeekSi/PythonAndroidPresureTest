from tkinter import *
import tkinter as tk
import tkinter.messagebox
import run
from constant import constants


def callback():
    if E1.get().strip() == '':
        tk.messagebox.showinfo("错误", "请输入包名")
        return
    if E2.get().strip() == '':
        tk.messagebox.showinfo("错误", "请输入压测时间,单位分钟")
        return
    global b1
    if run.isRunning:
        run.stop()
        b1['text'] = "开始监控"
    else:
        run.start(E1.get(), E2.get())
        b1['text'] = "停止任务"


def closeClient():
    if run.isRunning and tk.messagebox.askokcancel("提示", "关闭压测?"):
        run.stop()
        root.destroy()
    else:
        root.destroy()


def set_win_center(root, curWidth='', curHight=''):
    '''
    设置窗口大小，并居中显示
    :param root:主窗体实例
    :param curWidth:窗口宽度，非必填，默认200
    :param curHight:窗口高度，非必填，默认200
    :return:无
    '''
    if not curWidth:
        '''获取窗口宽度，默认200'''
        curWidth = root.winfo_width()
    if not curHight:
        '''获取窗口高度，默认200'''
        curHight = root.winfo_height()
    # print(curWidth, curHight)

    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)

    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 3
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    root.geometry(size_xy)


root = Tk()
root.title("性能压测")

f1 = Frame(root)
f1.place(x=10, y=20)
f2 = Frame(root)
f2.place(x=10, y=70)

f3 = Frame(root)
f3.place(x=10, y=130)

L1 = Label(f1, text="输入包名")
L1.pack(side=LEFT)
E1 = Entry(f1)
E1.pack(side=LEFT, padx=10)

L2 = Label(f2, text="输入时间")
L2.pack(side=LEFT)
E2 = Entry(f2)
E2.pack(side=LEFT, padx=10)

b1 = Button(root, text="开始监控", command=callback)
b1.place(x=300, y=40)

scroll = tkinter.Scrollbar(f3)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

text = Text(f3, width=60, height=15)
text.pack(side=tk.RIGHT, fill=tk.Y)
text.config(state='normal')

scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)

constants.text = text

set_win_center(root, 450, 360)

root.protocol("WM_DELETE_WINDOW", closeClient)

# 进入消息循环
root.mainloop()
