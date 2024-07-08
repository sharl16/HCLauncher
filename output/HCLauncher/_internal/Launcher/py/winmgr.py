import platform

if platform.system() != "Windows":
    sys.exit("Cannot run outside Windows")

import tkinter as tk
import threading
import sys

def show_splash(image_path, window_width, window_height):
    global root
    root = tk.Tk()
    root.image = tk.PhotoImage(file=image_path)
    global label
    label = tk.Label(root, image=root.image, bg='white')
    label.image = root.image
    root.overrideredirect(True)
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
    label.pack()
    root.mainloop()

def close_window(image_path):
    global root
    global label
    if root:
        new_image = tk.PhotoImage(file=image_path)
        label.config(image=new_image)
        label.image = new_image
    else:
        print("Root is not defined")

def close_windowr():
    print("Exiting")
    if root:
        root.quit()
    else:
        print("Root is not defined")
    sys.exit()

image_path = r'_internal\Launcher\py\Resources\HCGeneral.png'
window_width = 600
window_height = 282

splash_thread = threading.Thread(target=show_splash, args=(image_path, window_width, window_height))
splash_thread.start()
