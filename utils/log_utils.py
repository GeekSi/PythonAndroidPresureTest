from constant import constants
import tkinter as tk


def log(msg):
    print(msg)
    if constants.text is not None:
        constants.text.insert(tk.END, msg + "\n")
        constants.text.see(tk.END)
