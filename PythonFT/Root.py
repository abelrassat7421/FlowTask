import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
import time
import numpy as np

from Start import *
from Settings import *

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Flow Task v1.0')
        # self.iconbitmap('PythonFlowTask/target.ico')

        # Bind the Escape key to toggle fullscreen mode
        self.bind("<Escape>", self.toggle_fullscreen)

        #print(self.winfo_screenwidth()) # getting the scaled values in points, not the actual pixel resolution (factor x2 on Retina screen)
        #print(self.winfo_screenheight()) # method to get the actual number of pizels requires platform-specific approaches

        # window attributes & size
        # self.attributes("-topmost", True) # when window is open it will always be in front of any other existing window
        self.attributes("-fullscreen", True) # need terminal or IDE from where program executed not in full screen
        self.minsize(200, 100)

        # Probably change the names of these variables -> move to respective classes when needed
        dir_path = os.path.dirname(os.path.abspath(__file__))
        config_dir = "Configurations"
        output_dir = 'Output'
        Image_dir = "Images"
        target_file_name = "target2.png"
        #target_file_name = "target_color.png"
        self.TargetFilePath = os.path.join(dir_path, config_dir, Image_dir, target_file_name)
        triangle_file_name = "triangle.png"
        red_triangle_file_name = "red_triangle.png"
        triangle_rot_90 = "triangle_rot_90.png"
        triangle_rot_270 = "triangle_rot_270.png"
        red_triangle_rot_90 = "red_triangle_rot_90.png"
        red_triangle_rot_270 = "red_triangle_rot_270.png"
        self.RedTriangleFilePath = os.path.join(dir_path, config_dir, Image_dir, red_triangle_file_name)
        self.TriangleFilePath = os.path.join(dir_path, config_dir, Image_dir, triangle_file_name)
        self.TriangleRot90Path = os.path.join(dir_path, config_dir, Image_dir, triangle_rot_90)
        self.TriangleRot270Path = os.path.join(dir_path, config_dir, Image_dir, triangle_rot_270)
        self.RedTriangleRot90Path = os.path.join(dir_path, config_dir, Image_dir, red_triangle_rot_90)
        self.RedTriangleRot270Path = os.path.join(dir_path, config_dir, Image_dir, red_triangle_rot_270)

        cross_file_name = "cross.png"
        self.CrossFilePath = os.path.join(dir_path, config_dir, Image_dir, cross_file_name)
        config_file_name = "config.json"
        
        self.ConfigFilePath = os.path.join(dir_path, config_dir, config_file_name)
        self.ConfigDirPath = os.path.join(dir_path, config_dir)
        self.OutputPath = os.path.join(dir_path, output_dir)

        self.screen_width, self.screen_height = pyautogui.size()

        # Welcome window
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(expand=True, anchor='center')

        max_width = max(len("Start"), len("Settings"), len("Open Output Folder"), len("Close"))
        btn_start = ttk.Button(frm_buttons, text="Start", command=self.start, width=max_width)
        btn_settings = ttk.Button(frm_buttons, text="Settings", command=self.settings, width=max_width)
        btn_open_folder = ttk.Button(frm_buttons, text="Open Output Folder", command=self.open_folder, width=max_width)
        btn_close = ttk.Button(frm_buttons, text="Close", command=self.close_window, width=max_width)
        
        btn_start.pack(pady=5)
        btn_settings.pack(pady=5)
        btn_open_folder.pack(pady=5)
        btn_close.pack(pady=5)

    def start(self):
        StartWindow(self)

    def settings(self):
        SettingsWindow(master=self, json_file=self.ConfigFilePath)

    def open_folder(self):
        #subprocess.run(["open", self.OutputPath])
        os.startfile(self.OutputPath) # Windows Implementation
 
    def toggle_fullscreen(self, event=None):
        state = not self.attributes('-fullscreen')  
        self.attributes('-fullscreen', state)
        return "break"

    def clear_window(self):
        # Destroy each child widget in the main window
        for widget in self.winfo_children():
            widget.destroy()

    def close_window(self):
        self.attributes('-fullscreen', False)
        self.destroy()



