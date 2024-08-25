from tkinter import *
from tkinter import ttk

def Calculate():
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding = "3 3 12 12")

    