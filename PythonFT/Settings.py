import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
pyautogui.FAILSAFE = False
import time
import numpy as np
import subprocess
from Config import *

# Here better to have a new window open
class SettingsWindow:

    def __init__(self, master, json_file): 
        self.settings_window = tk.Toplevel(master)
        self.settings_window.title('Settings')
        #self.settings_window.focus_set() # Windows Implemetation
        self.settings_window.attributes('-fullscreen', True)
        # settings.iconbitmap('PythonFlowTask/target.ico') some settings/gear icon to add

        # Creating Config path for manual configuration of certain parameters
        dir_path = os.path.dirname(os.path.abspath(__file__))
        config_dir = "Configurations"
        config_file_name = "trial_by_trial_config.csv"
        self.ConfigFilePath = os.path.join(dir_path, config_dir, config_file_name)

        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self.settings_window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.settings_window, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.frm_settings = ttk.Frame(self.canvas, borderwidth=2, relief="ridge")
        self.canvas.create_window((0, 0), window=self.frm_settings, anchor='nw')

        # scrolling with mouse or top/down arrows
        self.frm_settings.bind('<Configure>', self.on_configure)
        
        # creating labels
        lbl_num_quest = tk.Label(master=self.frm_settings, text="Number of questions:")
        lbl_inverted = tk.Label(master=self.frm_settings, text="Is Inverted?:")
        lbl_trigger_visible = tk.Label(master=self.frm_settings, text="Trigger Visible?:")
        lbl_direction_triangles = tk.Label(master=self.frm_settings, text="Have triangles for direction?:") 
        lbl_configure_with_csv = tk.Label(master=self.frm_settings, text="Configure csv manually?:")
        lbl_trajectory_sampling_rate = tk.Label(master=self.frm_settings, text="Trajectory sampling rate (Hz):") 
        lbl_preparation_time = tk.Label(master=self.frm_settings, text="Preparation time before triangle appears:")
        lbl_inter_trial_time = tk.Label(master=self.frm_settings, text="Delay between trials:") 
        lbl_time_to_center = tk.Label(master=self.frm_settings, text="Time to Center of target:")
        lbl_triangle_time = tk.Label(master=self.frm_settings, text="Triangle time:") 
        lbl_num_random_trial = tk.Label(master=self.frm_settings, text="Number of Random Trials:")
        lbl_target_size = tk.Label(master=self.frm_settings, text="Target Size:")

        # creating canvas to delineate group of labels
        canvas1 = tk.Canvas(self.frm_settings, height=2, bg="white")
        canvas2 = tk.Canvas(self.frm_settings, height=2, bg="white")
        canvas3 = tk.Canvas(self.frm_settings, height=2, bg="white")
        canvas4 = tk.Canvas(self.frm_settings, height=2, bg="white")
        
        # placing labels 
        lbl_num_quest.grid(row=0, column=0, pady=2, sticky='w')
        canvas1.grid(row=2, column=0, sticky="ew", pady=(0, 0))
        lbl_inverted.grid(row=3, column=0, pady=2, sticky='w')
        lbl_trigger_visible.grid(row=4, column=0, pady=5, sticky='w')
        lbl_direction_triangles.grid(row=5, column=0, pady=2, sticky='w')
        canvas2.grid(row=6, column=0, sticky="ew", pady=(0, 0))
        lbl_configure_with_csv.grid(row=7, column=0, pady=2, sticky='w')
        canvas3.grid(row=9, column=0, sticky="ew", pady=(0, 0))
        lbl_trajectory_sampling_rate.grid(row=10, column=0, pady=2, sticky='w')
        lbl_preparation_time.grid(row=11, column=0, pady=2, sticky='w')
        lbl_inter_trial_time.grid(row=12, column=0, pady=2, sticky='w')
        lbl_time_to_center.grid(row=13, column=0, pady=2, sticky='w')
        lbl_triangle_time.grid(row=14, column=0, pady=2, sticky='w')
        lbl_num_random_trial.grid(row=15, column=0, pady=2, sticky='w')
        lbl_target_size.grid(row=16, column=0, pady=2, sticky='w')
        canvas4.grid(row=17, column=0, sticky="ew", pady=(0, 0))
        
        # drawing the lines
        canvas1.create_line(0, 1, canvas1.winfo_reqwidth(), 1, fill="black")
        canvas2.create_line(0, 1, canvas2.winfo_reqwidth(), 1, fill="black")
        canvas3.create_line(0, 1, canvas3.winfo_reqwidth(), 1, fill="black")
        canvas4.create_line(0, 1, canvas4.winfo_reqwidth(), 1, fill="black")

        # discrete set of options for dropdowns
        self.optionTF = [True, False]
        self.option_timing = ["pre", "post"]
        self.clk_num_quest = tk.IntVar()
        self.clk_inverted = tk.BooleanVar()
        self.clk_trigger_visible = tk.BooleanVar()
        self.clk_direction_triangles = tk.BooleanVar()
        self.clk_configure_with_csv = tk.BooleanVar()
        
        # creating entry boxes
        self.ent_trajectory_sampling_rate = ttk.Entry(self.frm_settings)
        self.ent_preparation_time = ttk.Entry(self.frm_settings)
        self.ent_inter_trial_time = ttk.Entry(self.frm_settings)
        self.ent_time_to_center = ttk.Entry(self.frm_settings)
        self.ent_triangle_time = ttk.Entry(self.frm_settings)
        self.ent_num_random_trial = ttk.Entry(self.frm_settings)
        self.ent_target_size = ttk.Entry(self.frm_settings)

        # Setting default values from json file
        with open(json_file, 'r') as file:
            data = json.load(file)
            
            self.clk_num_quest.set(data["num_questions"])
            self.clk_inverted.set(data["inverted"])
            self.clk_trigger_visible.set(data["trigger_visible"])
            self.clk_direction_triangles.set(data["direction_triangles"])
            self.clk_configure_with_csv.set(data["configure_with_csv"])
            self.ent_trajectory_sampling_rate.insert(0, data["trajectory_sampling_rate"])
            self.ent_preparation_time.insert(0, data["preparation_time"])
            self.ent_inter_trial_time.insert(0, data["inter-trial_time"])
            self.ent_time_to_center.insert(0, data["time_to_center_of_target"])
            self.ent_triangle_time.insert(0, data["triangle_time"])
            self.ent_num_random_trial.insert(0, data["num_random_trial"])
            self.ent_target_size.insert(0, data["target_size"])

        # creating option menus 
        drp_num_quest = ttk.OptionMenu(self.frm_settings, self.clk_num_quest, self.clk_num_quest.get(), *range(0, 11), command=self.update_questions)
        drp_inverted = ttk.OptionMenu(self.frm_settings, self.clk_inverted, self.clk_inverted.get(), *self.optionTF) 
        drp_trigger_visible = ttk.OptionMenu(self.frm_settings, self.clk_trigger_visible, self.clk_trigger_visible.get(), *self.optionTF)
        drp_direction_triangles = ttk.OptionMenu(self.frm_settings, self.clk_direction_triangles, self.clk_direction_triangles.get(), *self.optionTF, command=self.update_triangle_direction_param)
        drp_configure_with_csv = ttk.OptionMenu(self.frm_settings, self.clk_configure_with_csv, self.clk_configure_with_csv.get(), *self.optionTF, command=self.update_csv_config_options)

        # placing option menus and entry boxes
        drp_num_quest.grid(row=0, column=1, pady=2, padx=10, sticky='w')
        drp_inverted.grid(row=3, column=1, pady=2, padx=10, sticky='w')
        drp_trigger_visible.grid(row=4, column=1, pady=2, padx=10, sticky='w')
        drp_direction_triangles.grid(row=5, column=1, pady=2, padx=10,  sticky='w')
        drp_configure_with_csv.grid(row=7, column=1, pady=2, padx=10, sticky='w')
        self.ent_trajectory_sampling_rate.grid(row=10, column=1, pady=2, padx=10,  sticky='w')
        self.ent_preparation_time.grid(row=11, column=1, pady=2, padx=10,  sticky='w')
        self.ent_inter_trial_time.grid(row=12, column=1, pady=2, padx=10,  sticky='w')
        self.ent_time_to_center.grid(row=13, column=1, pady=2, padx=10, sticky='w')
        self.ent_triangle_time.grid(row=14, column=1, pady=2, padx=10, sticky='w')
        self.ent_num_random_trial.grid(row=15, column=1, pady=2, padx=10, sticky='w')
        self.ent_target_size.grid(row=16, column=1, pady=2, padx=10, sticky='w')

        # Create a frame to hold the Entry widgets and Option Menus that depend on other Option Menus 
        # i.e., second order widgets
        self.frame_questions = ttk.Frame(self.frm_settings)
        self.frame_not_config_with_csv = ttk.Frame(self.frm_settings)
        self.questions = []
        self.auto_config_param = {
            "mouse_appear_freq": 0, 
            "num_triggers": 0,
            "trigger_values": [],
            "num_triangle_target_interval": 0,
            "time_intervals": [], 
            "freq_false_directions": 0,
            }
        self.frame_questions.grid(row=1, column=0, columnspan=3, pady=2, padx=10,  sticky='w')
        self.frame_not_config_with_csv.grid(row=8, column=0, columnspan=2, pady=2, padx=10,  sticky='w')
        
        # Adding default values from json for second order widgets 
        with open(json_file, 'r') as file:
            data = json.load(file)
            
            if not self.clk_configure_with_csv.get(): 
                lbl_mouse_appear_freq = tk.Label(master=self.frame_not_config_with_csv, text="Mouse appearance frequency (%):") 
                lbl_num_trigger = tk.Label(master=self.frame_not_config_with_csv, text="Number of triggers:") 
                lbl_num_triangle_target_interval = tk.Label(master=self.frame_not_config_with_csv, text="Number of Triangle-to-Target time intervals:") 
                canvas = tk.Canvas(self.frame_not_config_with_csv , height=2, bg="white")

                lbl_mouse_appear_freq.grid(row=0, column=0, pady=2, sticky='w')
                canvas.grid(row=1, column=0, sticky="ew", pady=(0, 0))
                lbl_num_trigger.grid(row=2, column=0, pady=2, sticky='w')
                lbl_num_triangle_target_interval.grid(row=4, column=0, pady=2, sticky='w')

                canvas.create_line(0, 1, canvas.winfo_reqwidth(), 1, fill="black")
  
                self.clk_num_triggers = tk.IntVar()
                self.clk_num_triangle_target_interval = tk.IntVar() 
                self.ent_mouse_appear_freq = ttk.Entry(self.frame_not_config_with_csv)

                self.clk_num_triggers.set(data["num_triggers"])
                self.clk_num_triangle_target_interval.set(data["num_triangle_target_interval"])
                self.ent_mouse_appear_freq.insert(0, data["mouse_appear_freq"])
                drp_num_triggers = ttk.OptionMenu(self.frame_not_config_with_csv, self.clk_num_triggers, self.clk_num_triggers.get(), *range(1, 4), command=self.update_trigger_entries)
                drp_num_triangle_target_interval = ttk.OptionMenu(self.frame_not_config_with_csv, self.clk_num_triangle_target_interval, self.clk_num_triangle_target_interval.get(), *range(1, 4), command=self.update_time_intervals_entries)
                
                self.auto_config_param["mouse_appear_freq"] = self.ent_mouse_appear_freq
                self.auto_config_param["num_triggers"] = self.clk_num_triggers
                self.auto_config_param["num_triangle_target_interval"] = self.clk_num_triangle_target_interval
 
                self.ent_mouse_appear_freq.grid(row=0, column=1, pady=2, padx=10, sticky='w')
                drp_num_triggers.grid(row=2, column=1, pady=2, padx=10,  sticky='w')
                drp_num_triangle_target_interval.grid(row=4, column=1, pady=2, padx=10,  sticky='w')
                
                self.entry_frame_triggers = ttk.Frame(self.frame_not_config_with_csv)
                self.entry_frame_time_intervals = ttk.Frame(self.frame_not_config_with_csv)
                self.entry_frame_triangle_direction = ttk.Frame(self.frame_not_config_with_csv)
                self.entry_values_triggers = []
                self.entry_values_time_intervals = []
                self.ent_freq_false_directions = ttk.Entry(self.frame_not_config_with_csv)
                self.ent_freq_false_directions.insert(0, 0)
                self.entry_frame_triggers.grid(row=3, column=0, columnspan=2, pady=2, padx=10,  sticky='w')
                self.entry_frame_time_intervals.grid(row=5, column=0, columnspan=2, pady=2, padx=10,  sticky='w')
                self.entry_frame_triangle_direction.grid(row=7, column=0, columnspan=2, pady=2, padx=10,  sticky='w')
    
                for i in range(int(self.clk_num_triggers.get())):
                    label = ttk.Label(self.entry_frame_triggers, text=f"Position {i + 1} (%)")
                    entry = ttk.Entry(self.entry_frame_triggers)
                    entry.insert(0, data["trigger_values"][i])
                    self.entry_values_triggers.append(entry)
                    label.grid(row=i, column=0, pady=2, padx=10, sticky='w')
                    entry.grid(row=i, column=1, pady=2, padx=10, sticky='w')

                for i in range(int(self.clk_num_triangle_target_interval.get())):
                    label = ttk.Label(self.entry_frame_time_intervals, text=f"Time {i + 1} (ms)")
                    entry = ttk.Entry(self.entry_frame_time_intervals)
                    entry.insert(0, data["time_intervals"][i])
                    self.entry_values_time_intervals.append(entry)
                    label.grid(row=i, column=0, pady=2, padx=10, sticky='w')
                    entry.grid(row=i, column=1, pady=2, padx=10, sticky='w')
                
                if self.clk_direction_triangles.get():
                    lbl_freq_false_directions = tk.Label(master=self.entry_frame_triangle_direction, text="Frequency of false directions (%):") 
                    lbl_freq_false_directions.grid(row=0, column=0, pady=2, sticky='w')
                    self.ent_freq_false_directions = ttk.Entry(self.entry_frame_triangle_direction)
                    self.ent_freq_false_directions.insert(0, data["freq_false_directions"])
                    self.ent_freq_false_directions.grid(row=0, column=1, pady=2, sticky='w')

                self.auto_config_param["trigger_values"] = self.entry_values_triggers
                self.auto_config_param["time_intervals"] = self.entry_values_time_intervals
                self.auto_config_param["freq_false_directions"] = self.ent_freq_false_directions
                
            for i in range(int(self.clk_num_quest.get())):
                label = ttk.Label(self.frame_questions, text=f"Question {i + 1}:")
                sublabel_quest_timing = ttk.Label(self.frame_questions, text=f"Question timing:")
                sublabel_quest_formulation = ttk.Label(self.frame_questions, text=f"Question formulation:")
                sublabel_answer_range = ttk.Label(self.frame_questions, text=f"Answer range from 1 to ... :")

                clk_timing = tk.StringVar()
                clk_timing.set(data["questions"][i]["timing"])
                drp_timing = ttk.OptionMenu(self.frame_questions, clk_timing, clk_timing.get(), *self.option_timing)
                entry_quest_formulation = ttk.Entry(self.frame_questions)
                entry_quest_formulation.insert(0, data["questions"][i]["formulation"])
                clk_answer_range = tk.IntVar()
                clk_answer_range.set(data["questions"][i]["answer_range"])
                drp_answer_range = ttk.OptionMenu(self.frame_questions, clk_answer_range, clk_answer_range.get(), *range(2, 10))
                self.questions.append({ 
                    "timing": clk_timing,
                    "formulation": entry_quest_formulation,
                    "answer_range": clk_answer_range
                })
                label.grid(row=4*i + i, column=0, pady=2, padx=10, sticky='w')
                sublabel_quest_timing.grid(row=4*i + i+1, column=1, pady=2, padx=10, sticky='w')
                drp_timing.grid(row=4*i + i+1, column=2, pady=2, padx=10, sticky='w')
                sublabel_quest_formulation.grid(row=4*i + i+2, column=1, pady=2, padx=10, sticky='w')
                entry_quest_formulation.grid(row=4*i + i+2, column=2, pady=2, padx=10, sticky='w')
                sublabel_answer_range.grid(row=4*i + i+3, column=1, pady=2, padx=10, sticky='w')
                drp_answer_range.grid(row=4*i + i+3, column=2, pady=2, padx=10, sticky='w')

        btn_open_config = ttk.Button(self.frm_settings, text="Open config file", command=self.open_config)
        btn_open_config.grid(row=18, column=0, pady=10, padx=20, sticky='w')

        btn_save = ttk.Button(self.frm_settings, text="Save", command=self.save_settings)
        btn_save.grid(row=19, column=0, pady=2, padx=20, sticky='w')

        btn_close = ttk.Button(self.frm_settings, text="Close", command=self.close_settings_window)
        btn_close.grid(row=20, column=0, pady=2, padx=20, sticky='w')

        lbl_remark = tk.Label(master=self.frm_settings, text="NB: Pour référence, la croix de départ se situe à 5% de la hauteur de l'écran et tous les temps sont en (ms).", font=("Arial", 12, "italic"))
        lbl_remark.grid(row=21, column=0, pady=10, padx=20, sticky='w')

    def on_configure(self, event):
        # Set the scroll region after UI has been configured
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def update_csv_config_options(self, value):
        if not self.clk_configure_with_csv.get(): 
            lbl_mouse_appear_freq = tk.Label(master=self.frame_not_config_with_csv, text="Mouse appearance frequency (%):") 
            lbl_num_trigger = tk.Label(master=self.frame_not_config_with_csv, text="Number of triggers:") 
            lbl_num_triangle_target_interval = tk.Label(master=self.frame_not_config_with_csv, text="Number of Triangle-to-Target time intervals:") 
            canvas = tk.Canvas(self.frame_not_config_with_csv , height=2, bg="white")

            lbl_mouse_appear_freq.grid(row=0, column=0, pady=2, sticky='w')
            canvas.grid(row=1, column=0, sticky="ew", pady=(0, 0))
            lbl_num_trigger.grid(row=2, column=0, pady=2, sticky='w')
            lbl_num_triangle_target_interval.grid(row=4, column=0, pady=2, sticky='w')

            canvas.create_line(0, 1, canvas.winfo_reqwidth(), 1, fill="black")

            self.clk_num_triggers = tk.IntVar()
            self.clk_num_triggers.set(1)
            self.clk_num_triangle_target_interval = tk.IntVar() 
            self.clk_num_triangle_target_interval.set(1)
            self.ent_mouse_appear_freq = ttk.Entry(self.frame_not_config_with_csv)

            drp_num_triggers = ttk.OptionMenu(self.frame_not_config_with_csv, self.clk_num_triggers, self.clk_num_triggers.get(), *range(1, 4), command=self.update_trigger_entries)
            drp_num_triangle_target_interval = ttk.OptionMenu(self.frame_not_config_with_csv, self.clk_num_triangle_target_interval, self.clk_num_triangle_target_interval.get(), *range(1, 4), command=self.update_time_intervals_entries)

            self.auto_config_param["mouse_appear_freq"] = self.ent_mouse_appear_freq
            self.auto_config_param["num_triggers"] = self.clk_num_triggers
            self.auto_config_param["num_triangle_target_interval"] = self.clk_num_triangle_target_interval

            self.ent_mouse_appear_freq.grid(row=0, column=1, pady=2, padx=10, sticky='w')
            drp_num_triggers.grid(row=2, column=1, pady=2, padx=10,  sticky='w')
            drp_num_triangle_target_interval.grid(row=4, column=1, pady=2, padx=10,  sticky='w')

            self.entry_frame_triggers = ttk.Frame(self.frame_not_config_with_csv)
            self.entry_frame_time_intervals = ttk.Frame(self.frame_not_config_with_csv)
            self.entry_frame_triangle_direction = ttk.Frame(self.frame_not_config_with_csv)
            self.entry_values_triggers = []
            self.entry_values_time_intervals = []
            self.ent_freq_false_directions = ttk.Entry(self.frame_not_config_with_csv)
            self.ent_freq_false_directions.insert(0, 0)
            self.entry_frame_triggers.grid(row=3, column=0, columnspan=2, pady=2, padx=10,  sticky='w')
            self.entry_frame_time_intervals.grid(row=5, column=0, columnspan=2, pady=2, padx=10,  sticky='w')
            self.entry_frame_triangle_direction.grid(row=6, column=0, columnspan=2, pady=2, padx=10,  sticky='w')

            for i in range(int(self.clk_num_triggers.get())):
                label = ttk.Label(self.entry_frame_triggers, text=f"Position {i + 1} (%)")
                entry = ttk.Entry(self.entry_frame_triggers)
                self.entry_values_triggers.append(entry)
                label.grid(row=i, column=0, pady=2, padx=10, sticky='w')
                entry.grid(row=i, column=1, pady=2, padx=10, sticky='w')

            for i in range(int(self.clk_num_triangle_target_interval.get())):
                label = ttk.Label(self.entry_frame_time_intervals, text=f"Time {i + 1} (ms)")
                entry = ttk.Entry(self.entry_frame_time_intervals)
                self.entry_values_time_intervals.append(entry)
                label.grid(row=i, column=0, pady=2, padx=10, sticky='w')
                entry.grid(row=i, column=1, pady=2, padx=10, sticky='w')
            
            if self.clk_direction_triangles.get():
                lbl_freq_false_directions = tk.Label(master=self.entry_frame_triangle_direction, text="Frequency of false directions (%):") 
                lbl_freq_false_directions.grid(row=0, column=0, pady=2, sticky='w')
                self.ent_freq_false_directions = ttk.Entry(self.entry_frame_triangle_direction)
                self.ent_freq_false_directions.grid(row=0, column=1, pady=2, sticky='w')
            
            self.auto_config_param["trigger_values"] = self.entry_values_triggers
            self.auto_config_param["time_intervals"] = self.entry_values_time_intervals
            self.auto_config_param["freq_false_directions"] = self.ent_freq_false_directions

        else:
            # Destroy existing Entry widgets
            for widget in self.frame_not_config_with_csv.winfo_children():
               widget.destroy() 

    def update_questions(self, value):
        # Destroy existing widgets
        for widget in self.frame_questions.winfo_children():
            widget.destroy()
            self.questions.clear()
        # Create new widgets
        for i in range(int(value)):
            label = ttk.Label(self.frame_questions, text=f"Question {i + 1}:")
            sublabel_quest_timing = ttk.Label(self.frame_questions, text=f"Question timing:")
            sublabel_quest_formulation = ttk.Label(self.frame_questions, text=f"Question formulation:")
            sublabel_answer_range = ttk.Label(self.frame_questions, text=f"Answer range:")

            clk_timing = tk.StringVar()
            drp_timing = ttk.OptionMenu(self.frame_questions, clk_timing, self.option_timing[0], *self.option_timing)
            entry_quest_formulation = ttk.Entry(self.frame_questions)
            clk_answer_range = tk.IntVar()
            clk_answer_range.set(2)
            drp_answer_range = ttk.OptionMenu(self.frame_questions, clk_answer_range, clk_answer_range.get(), *range(2, 10))
            self.questions.append({ 
                "timing": clk_timing,
                "formulation": entry_quest_formulation,
                "answer_range": clk_answer_range
            })
            label.grid(row=4*i + i, column=0, pady=2, padx=10, sticky='w')
            sublabel_quest_timing.grid(row=4*i + i+1, column=1, pady=2, padx=10, sticky='w')
            drp_timing.grid(row=4*i + i+1, column=2, pady=2, padx=10, sticky='w')
            sublabel_quest_formulation.grid(row=4*i + i+2, column=1, pady=2, padx=10, sticky='w')
            entry_quest_formulation.grid(row=4*i + i+2, column=2, pady=2, padx=10, sticky='w')
            sublabel_answer_range.grid(row=4*i + i+3, column=1, pady=2, padx=10, sticky='w')
            drp_answer_range.grid(row=4*i + i+3, column=2, pady=2, padx=10, sticky='w')

    def update_trigger_entries(self, value):
        # Destroy existing Entry widgets
        for widget in self.entry_frame_triggers.winfo_children():
            widget.destroy()
            self.entry_values_triggers.clear()
        # Create new Entry widgets
        for i in range(int(value)):
            label = ttk.Label(self.entry_frame_triggers, text=f"Position {i + 1} (%)")
            entry = ttk.Entry(self.entry_frame_triggers)
            self.entry_values_triggers.append(entry)
            label.grid(row=i, column=0, pady=2, padx=10, sticky='w')
            entry.grid(row=i, column=1, pady=2, padx=10, sticky='w')

    def update_time_intervals_entries(self, value):
       # Destroy existing Entry widgets
        for widget in self.entry_frame_time_intervals.winfo_children():
            widget.destroy()
            self.entry_values_time_intervals.clear()
        # Create new Entry widgets
        for i in range(int(value)):
            label = ttk.Label(self.entry_frame_time_intervals, text=f"Time {i + 1} (ms)")
            entry = ttk.Entry(self.entry_frame_time_intervals)
            self.entry_values_time_intervals.append(entry)
            label.grid(row=i, column=0, pady=2, padx=10, sticky='w')
            entry.grid(row=i, column=1, pady=2, padx=10, sticky='w')

    def update_triangle_direction_param(self, value):
        # delete this function and have changes of value display frequency of false directions if config manually false and direction triangles true
        if self.clk_direction_triangles.get() and not self.clk_configure_with_csv.get():
            lbl_freq_false_directions = tk.Label(master=self.entry_frame_triangle_direction, text="Frequency of false directions (%):") 
            lbl_freq_false_directions.grid(row=0, column=0, pady=2, sticky='w')
            self.ent_freq_false_directions = ttk.Entry(self.entry_frame_triangle_direction)
            self.ent_freq_false_directions.grid(row=0, column=1, pady=2, sticky='w')
            self.auto_config_param["freq_false_directions"] = self.ent_freq_false_directions
        else:
            # Destroy existing Entry widgets
            for widget in self.entry_frame_triangle_direction.winfo_children():
               widget.destroy() 

    def open_config(self):
        subprocess.run(["open", self.ConfigFilePath])
        #os.startfile(self.ConfigFilePath) # Windows Implementation

    def save_settings(self):        
        val_num_questions = self.clk_num_quest.get()
        val_questions = []
        for quest in self.questions:
            if isinstance(quest["timing"], tk.StringVar):
                quest["timing"] = quest["timing"].get()
            if isinstance(quest["formulation"], ttk.Entry):
                quest["formulation"] = quest["formulation"].get()
            if isinstance(quest["answer_range"], tk.IntVar):
                quest["answer_range"] = quest["answer_range"].get()

            val_questions.append({ 
                "timing": str(quest["timing"]),
                "formulation": str(quest["formulation"]),
                "answer_range": int(quest["answer_range"])
            })
        val_inverted = self.clk_inverted.get()
        val_trigger_visible = self.clk_trigger_visible.get()
        val_direction_triangles = self.clk_direction_triangles.get()
        val_configure_with_csv = self.clk_configure_with_csv.get()
        if not val_configure_with_csv:
            val_mouse_appear_freq = self.auto_config_param["mouse_appear_freq"].get()
            val_num_triggers = self.auto_config_param["num_triggers"].get()
            val_triggers = [int(entry.get()) for entry in self.auto_config_param["trigger_values"]]
            val_num_triangle_target_interval = self.auto_config_param["num_triangle_target_interval"].get()
            val_time_intervals = [int(entry.get()) for entry in self.auto_config_param["time_intervals"]]
            val_freq_false_directions = self.auto_config_param["freq_false_directions"].get()
        val_trajectory_sampling_rate = self.ent_trajectory_sampling_rate.get()
        val_preparation_time = self.ent_preparation_time.get()
        val_inter_trial_time = self.ent_inter_trial_time.get()
        val_time_to_center = self.ent_time_to_center.get()
        val_triangle_time = self.ent_triangle_time.get()
        val_num_random_trial = self.ent_num_random_trial.get()
        val_target_size = self.ent_target_size.get()

        # Read the existing JSON data
        dir_path = os.path.dirname(os.path.abspath(__file__))
        config_dir = "Configurations"
        file_name = "config.json"
        FilePath = os.path.join(dir_path, config_dir, file_name)
        with open(FilePath, 'r') as file:
            data = json.load(file)

        # Update the values
        data["num_questions"] = val_num_questions
        data["questions"] = val_questions
        data["inverted"] = val_inverted
        data["trigger_visible"] = val_trigger_visible
        data["direction_triangles"] = val_direction_triangles
        data["configure_with_csv"] = val_configure_with_csv
        if not val_configure_with_csv:
            data["mouse_appear_freq"] = float(val_mouse_appear_freq)
            data["num_triggers"] = val_num_triggers
            data["trigger_values"] = val_triggers
            data["num_triangle_target_interval"] = val_num_triangle_target_interval
            data["time_intervals"] = val_time_intervals
            data["freq_false_directions"] = float(val_freq_false_directions)
        data["trajectory_sampling_rate"] = int(val_trajectory_sampling_rate)
        data["preparation_time"] = int(val_preparation_time)
        data["inter-trial_time"] = int(val_inter_trial_time)
        data["time_to_center_of_target"] = int(val_time_to_center)
        data["triangle_time"] = int(val_triangle_time)
        data["num_random_trial"] = int(val_num_random_trial)
        data["target_size"] = int(val_target_size)

        # Write the updated data back to the JSON file
        with open(FilePath, 'w') as file:
            json.dump(data, file, indent=4)

    def close_settings_window(self):
        self.settings_window.destroy()


   

