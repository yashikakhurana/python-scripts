# Author: [Yashika Khurana](https://github.com/yashikakhurana)

import webbrowser
import tkinter as tk
from tkinter import filedialog


def open_file():
    # file dialog
    file_path = filedialog.askopenfilename()
    # read file
    with open(file_path, "r") as file:
        for line in file:
            webbrowser.open_new_tab(line.strip())


root = tk.Tk()
root.title("Link Opener")
root.geometry("400x300")

button = tk.Button(
    root, text="Select a file from which you want to load bookmarks", command=open_file)
button.pack(pady=100)

root.mainloop()
