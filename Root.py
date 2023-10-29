import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
import time
import numpy as np

from Config import *
from Start import *
from Settings import *

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Flow Task v1.0')
        # self.iconbitmap('PythonFlowTask/target.ico')

        # Bind the Escape key to toggle fullscreen mode
        self.bind("<Escape>", self.toggle_fullscreen)

        # print(self.winfo_screenwidth()) # getting the scaled values in points, not the actual pixel resolution (factor x2 on Retina screen)
        # print(self.winfo_screenheight()) # method to get the actual number of pizels requires platform-specific approaches

        # window attributes & size
        # self.attributes("-topmost", True) # when window is open it will always be in front of any other existing window
        self.attributes("-fullscreen", True) # need terminal or IDE from where program executed not in full screen
        self.minsize(200, 100)
        # self.overrideredirect(True) # removing the title bar 

        # Probably change the names of these variables -> move to respective classes when needed
        dir_path = os.path.dirname(os.path.abspath(__file__))
        target_file_name = "target2.png"
        #target_file_name = "target_color.png"
        Image_dir = "Images"
        self.TargetFilePath = os.path.join(dir_path, Image_dir, target_file_name)
        triangle_file_name = "triangle.png"
        self.TriangleFilePath = os.path.join(dir_path, Image_dir, triangle_file_name)
        cross_file_name = "cross.png"
        self.CrossFilePath = os.path.join(dir_path, Image_dir, cross_file_name)
        config_file_name = "config.json"
        gen_config_file_name = 'trial_by_trial_config.csv'
        config_dir = "Configurations"
        self.ConfigFilePath = os.path.join(dir_path, config_dir, config_file_name)
        self.GenConfigFilePath = os.path.join(dir_path, config_dir, gen_config_file_name)

        self.screen_width, self.screen_height = pyautogui.size()

        # Welcome window
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(expand=True, anchor='center')

        max_width = max(len("Start"), len("Settings"), len("Open Folder"))
        btn_start = ttk.Button(frm_buttons, text="Start", command=self.start, width=max_width)
        btn_settings = ttk.Button(frm_buttons, text="Settings", command=self.settings, width=max_width)
        btn_start.pack(pady=5)
        btn_settings.pack(pady=5)

    def start(self):
        StartWindow(self)

    def settings(self):
        SettingsWindow(master=self, json_file=self.ConfigFilePath)
 
    def toggle_fullscreen(self, event=None):
        state = not self.attributes('-fullscreen')  
        self.attributes('-fullscreen', state)
        return "break"

    def clear_window(self):
        # Destroy each child widget in the main window
        for widget in self.winfo_children():
            widget.destroy()



