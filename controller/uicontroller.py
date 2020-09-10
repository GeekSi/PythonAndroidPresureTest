import tkinter as tk

text = None

btn = None


def setBtnText(str):
    global btn
    if btn is not None:
        btn['text'] = str


def appendText(str):
    global text
    if text is not None:
        text.insert(tk.END, str + "\n")
        text.see(tk.END)
