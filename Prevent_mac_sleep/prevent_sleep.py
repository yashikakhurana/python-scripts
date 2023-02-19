import tkinter as tk
import pyautogui
import subprocess  # to avoid sleep for mac
# import win32api # to make process busy for windows
# import win32con # to make process bust for windows


class App:
    def __init__(self, master):
        self.master = master
        master.title("Prevent Sleep App")
        root.geometry("400x300")

        # Create buttons
        self.start_button = tk.Button(
            master, text="Start", command=self.start_moving_mouse)
        self.stop_button = tk.Button(
            master, text="Stop", command=self.stop_moving_mouse, state="disabled")
        self.start_button.pack()
        self.stop_button.pack()

        # Set up mouse movement
        self.mouse_moving = False

    def start_moving_mouse(self):
        self.mouse_moving = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.move_mouse()
        # Prevent system from going to sleep for mac
        subprocess.Popen(["caffeinate", "-dims"])

        # Prevent system from going to sleep for windows
        # win32api.SetThreadExecutionState(
        #     win32con.ES_CONTINUOUS | win32con.ES_SYSTEM_REQUIRED)

    def stop_moving_mouse(self):
        self.mouse_moving = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        # Allow system to go to sleep for mac
        subprocess.Popen(["killall", "caffeinate"])
        # Allow system to go to sleep for windows
        # win32api.SetThreadExecutionState(win32con.ES_CONTINUOUS)

    def move_mouse(self):
        if self.mouse_moving:
            pyautogui.move(1000, 1000, 2)

            # Move mouse every minute
            self.master.after(3, self.move_mouse)


# Create and run the app
root = tk.Tk()
app = App(root)
root.mainloop()
