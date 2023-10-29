import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
import time
import numpy as np
import random
import sys

import ctypes # Windows implementation
import subprocess

from Config import *
from Questions import *
#from Root import *

# Define the RECT structure to immobilize the mouse
# Windows implementation
"""
class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]
"""
                
# Windows implementation 
# Load user32.dll for blocking mouse
# user32 = ctypes.windll.user32

class StartWindow:
    def __init__(self, master):
        # Continue to operate on the master window
        self.root = master
        self.root.clear_window()
        self.screen_width = self.root.screen_width
        self.screen_height = self.root.screen_height
        self.config = Config(self.root.ConfigFilePath, self.root) 

        self.target_set = False
        self.target_center_reached = False 
        self.get_ready = False
        self.recording = False
        self.trigger_set = False 
        self.trial_counter = 0 
        self.seconds_elapsed = 0
        self.time_in_target = 0
        self.can_skip_next_trial = False
        self.after_wait_enter_target = False
        self.after_wait_end_trial = False
        
        self.Questions = self.config.questions 
        self.Inverted = self.config.inverted # this may be converted into a list 
        self.TriggerVisible = self.config.trigger_visible 
        self.ConfigWithCSV = self.config.configure_with_csv 
        if not self.ConfigWithCSV: 
            self.MouseAppearFreq = self.config.mouse_appear_freq
            self.TriggerPosVal = self.config.trigger_values 
            self.TriangleTargetIntervalVal = self.config.time_intervals # Time between the triangle disappearing and target appearing (mouse de-frozen)
        self.TrajSamplingRate = self.config.trajectory_sampling_rate
        self.PreparationTime = self.config.preparation_time # Time before triangle appears 
        self.InterTrialTime = self.config.inter_trial_time # Time between pre and post questions
        self.TimeToCenterTarget = self.config.time_to_center_of_target 
        self.TriangleTime = self.config.triangle_time # Time triangle appears for
        self.NumTrials = self.config.num_random_trial
        if not self.ConfigWithCSV:
            self.gen_csv_config_file()
        self.TargetPos, self.MouseAppears, self.TriggerPos, self.TriangleTargetInterval = self.config.read_config(self.root.GenConfigFilePath)
        # adjusting trigger position (0 top, 1 bottom)
        self.TriggerPos = [1-(trig_pos/100) for trig_pos in self.TriggerPos]
        self.target_pos_dic = {0:0.15, 1:0.5, 2:0.85}
        # Preload and process images outside the update_timer function
        self.TargetSize = self.config.target_size
        TriangleSize = 150
        self.CrossSize = 20
        self.image_tar = Image.open(self.root.TargetFilePath).convert("RGBA")
        image_tri = Image.open(self.root.TriangleFilePath)
        image_cross = Image.open(self.root.CrossFilePath).convert("RGBA")
        self.image_tar_resized = self.image_tar.resize((self.TargetSize, self.TargetSize))
        image_tri_resized = image_tri.resize((TriangleSize, TriangleSize))
        self.image_cross_resized = image_cross.resize((self.CrossSize, self.CrossSize))
        
        self.img_target_preloaded = ImageTk.PhotoImage(self.image_tar_resized)
        self.img_triangle_preloaded = ImageTk.PhotoImage(image_tri_resized)
        self.img_cross_preloaded = ImageTk.PhotoImage(self.image_cross_resized)

        # Create a canvas that spans the entire width of the window 
        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg=self.root.cget('bg'))
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set the black starting box
        self.frm_starting_block = tk.Frame(master=self.canvas, width=200, height=100, bg="#3E3C44")
        self.frm_starting_block.pack_propagate(0) # Prevent the frame from resizing to fit its contents
        self.frm_starting_block.place(relx=0.5, rely=1, anchor='s')
        
        self.lbl_triangle = tk.Label(master=self.canvas)
        self.lbl_cross = tk.Label(master=self.canvas, bg="#3E3C44", borderwidth=0)
        self.lbl_cross.place(relx=0.5, rely=0.95, anchor='center')
        self.lbl_cross.config(image=self.img_cross_preloaded)
        self.lbl_cross.image = self.img_cross_preloaded
        self.root.update_idletasks()
        self.cross_center = (round(0.5*self.screen_width), round(0.95*self.screen_height))

        # Bind space bar to move to the following trial
        self.root.bind("<space>", self.on_space_press)

        self.root.bind("<Return>", self.on_enter_key)
        
        '''
        # Create a label for the timer
        self.lbl_timer = tk.Label(master=self.canvas, text="0")
        self.lbl_timer.place(relx=0.95, rely=0.95, anchor='se') 
        '''

        self.global_update()

    def new_trial(self):
        if self.trial_counter > 0:
           self.clear_canvas()
        self.target_set = False
        self.target_center_reached = False
        self.get_ready = True 
        self.trigger_set = False

    def draw_line(self, event=None):
        self.trigger_line = self.canvas.create_line(0, self.canvas.winfo_height()*self.TriggerPos[self.trial_counter], self.canvas.winfo_width(), self.canvas.winfo_height()*self.TriggerPos[self.trial_counter], fill="black", dash=(10))

    def capture_trajectory(self, sampling_rate=100): 
        coordinates = []
        img = Image.new("RGB", (self.screen_width, self.screen_height), "white")
        draw = ImageDraw.Draw(img)
        self.root.update_idletasks()
        _, _, _, a = self.image_tar_resized.split()
        img.paste(self.image_tar_resized, (round(self.lbl_target.winfo_rootx() - 0.5*self.TargetSize), round(self.lbl_target.winfo_rooty() - 0.4*self.TargetSize)), mask=a)
        _, _, _, a = self.image_cross_resized.split()
        img.paste(self.image_cross_resized, (round(self.screen_width*0.5 - 0.5*self.CrossSize), round(0.95*self.screen_height - 0.5*self.CrossSize)), mask=a)

        self.interval = int(1000 / sampling_rate) # in ms
        self.start_time = time.time()
        # Store the previous position to draw a line between points
        prev_x, prev_y = pyautogui.position()
        coordinates.append((prev_x, prev_y))

        self.recording = True
        self.record_and_draw_last_traj_pt(draw, coordinates, prev_x, prev_y, img)

    def record_and_draw_last_traj_pt(self, draw, coordinates, prev_x, prev_y, img):
        if self.recording == True:
            x, y = pyautogui.position()
            coordinates.append((x, y))
            # Draw a line from the previous position to the current position
            draw.line([(prev_x, prev_y), (x, y)], fill="black", width=2)
            if self.target_center_reached == True: 
                self.recording = False
                self.save_trajectory_info(coordinates, img)
            self.root.after(self.interval, lambda: self.record_and_draw_last_traj_pt(draw, coordinates, x, y, img))
        
    def save_trajectory_info(self, coordinates, img):
        num = str(self.trial_counter + 1).zfill(2)
        traj_file_name = f"mouse_trajectory_{num}.png"
        dir_path = os.path.dirname(os.path.abspath(__file__))
        dir_output = "Output"
        dir_trajectories = "Trajectories"
        TrajFilePath = os.path.join(dir_path, dir_output, dir_trajectories, traj_file_name)
        traj_coord_file_name = f"mouse_trajectory_coord_{num}.csv"
        TrajCoordFilePath = os.path.join(dir_path, dir_output, dir_trajectories, traj_coord_file_name)
        
        with open(TrajCoordFilePath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['X', 'Y']) 
            writer.writerows(coordinates)  
        #print(f'Data saved to {TrajCoordFilePath}')
        img.save(TrajFilePath)
        #print("Trajectory saved as", f"mouse_trajectory_{num}.png")

    def is_point_in_start_block(self, x, y):
        frame_x = self.frm_starting_block.winfo_rootx()
        frame_y = self.frm_starting_block.winfo_rooty()
        frame_width = self.frm_starting_block.winfo_width()
        frame_height = self.frm_starting_block.winfo_height()
        return frame_x <= x <= frame_x + frame_width and frame_y <= y <= frame_y + frame_height
    
    def clear_canvas(self):
        self.lbl_target.place_forget()
        # the trigger isn't a widget 
        if self.TriggerVisible and self.trigger_set:
            self.canvas.delete(self.trigger_line) 
    
    def restart_window(self):
        self.root.attributes('-fullscreen', False)
        self.root.destroy()
        os.execv(sys.executable, ['python'] + sys.argv)

    def on_space_press(self, event):
        if self.can_skip_next_trial:
            # to finish recording the trajectory
            self.target_center_reached = True 
            if self.after_wait_enter_target:
                self.root.after_cancel(self.after_wait_enter_target)
            if self.after_wait_end_trial:
                self.root.after_cancel(self.after_wait_end_trial)
            self.move_next_trial()
    
    def on_enter_key(self, event):
        self.restart_window()

    def pre_trial_questions_and_start(self):
        is_there_quest, quest_type = self.is_there_question_type("pre")
        if is_there_quest:
            questions_window = QuestionsWindow(master=self.root, trial_num=self.trial_counter, timing="pre", quest_type=quest_type)
            self.root.wait_window(questions_window.window)  
        if self.TriggerVisible and not self.trigger_set: 
            self.draw_line() 
            self.trigger_set = True 
        self.move_mouse_to_start()

    def move_mouse_to_start(self):
        self.lbl_transition.pack_forget()
        pyautogui.moveTo(self.cross_center)
        self.lbl_target = tk.Label(master=self.canvas, borderwidth=0)
        self.lbl_decoy_target = tk.Label(master=self.canvas)
        self.lbl_target.place(relx=self.target_pos_dic[self.TargetPos[self.trial_counter]], rely=0.2, anchor='center') 
        self.lbl_decoy_target.place(relx=0.5, rely=0.2, anchor='center')
        #lock_cursor_to_rect(self.cross_center[0], self.cross_center[1], 1, 1) # Windows implementation
        self.trial_update() 

    def is_there_question_type(self, question_timing):
        is_there_quest = False
        quest_type = []
        for entry in self.Questions:
            if entry.get('timing') == question_timing:
                is_there_quest = True
                quest_type.append(entry) 
        return is_there_quest, quest_type 

    def is_target_center_reached(self, x, y):
        target_x = self.lbl_target.winfo_rootx()
        target_y = self.lbl_target.winfo_rooty()
        target_width = self.TargetSize
        target_height = self.TargetSize
        center_x = target_x + target_width / 2
        center_y = target_y + target_height / 2
        # the center of the target icon is 1/5 its size
        region_width = target_width / 5
        region_height = target_height / 5
        in_center_region = (
            center_x - region_width / 2 <= x <= center_x + region_width / 2 and
            center_y - region_height / 2 <= y <= center_y + region_height / 2
        )
        return in_center_region
    
    def is_target_reached(self, x, y):
        target_x = self.lbl_target.winfo_rootx()
        target_y = self.lbl_target.winfo_rooty()
        target_width = self.lbl_target.winfo_width()
        target_height = self.lbl_target.winfo_height()
        center_x = target_x + target_width / 2
        center_y = target_y + target_height / 2
        in_region = (
            center_x - target_width / 2 <= x <= center_x + target_width / 2 and
            center_y - target_height / 2 <= y <= center_y + target_height / 2
        )
        return in_region
    
    def show_target_based_on_pos(self):
        self.seconds_elapsed += 0.1
        # self.lbl_timer.config(text=str(int(self.seconds_elapsed)))
        _, y = pyautogui.position()
        if self.recording == False:
            self.capture_trajectory(sampling_rate=self.TrajSamplingRate)
        # Check if the mouse is above the trigger
        if y < (self.TriggerPos[self.trial_counter]) * self.screen_height:
            # unpack centered decoy target image
            self.lbl_decoy_target.place_forget()
            # set new target image
            self.lbl_target.config(image=self.img_target_preloaded)
            self.lbl_target.image = self.img_target_preloaded
            self.target_set = True
            self.can_skip_next_trial = True
            self.wait_enter_target()
        else:
            self.root.after(100, lambda: self.show_target_based_on_pos())

    def wait_enter_target(self):
        x, y = pyautogui.position()
        self.seconds_elapsed += 0.01
        # self.lbl_timer.config(text=str(int(self.seconds_elapsed)))
        if self.is_target_reached(x, y):
            self.wait_end_trial()
        else:
            self.after_wait_enter_target = self.root.after(10, lambda: self.wait_enter_target())
           
    def wait_end_trial(self):
        self.time_in_target += 10 
        self.seconds_elapsed += 0.01
        # self.lbl_timer.config(text=str(int(self.seconds_elapsed)))
        x, y = pyautogui.position()
        #if self.is_target_center_reached(x, y) or self.time_in_target >= self.TimeToCenterTarget:
        if self.time_in_target >= self.TimeToCenterTarget:
            self.target_center_reached = True
            self.can_skip_next_trial = False
            self.move_next_trial()
            # self.lbl_timer.config(text=str(self.seconds_elapsed) 
        else:
            self.after_wait_end_trial = self.root.after(10, lambda: self.wait_end_trial())

    def move_next_trial(self):
        if not self.MouseAppears[self.trial_counter]:
            self.root.config(cursor="")
        if self.Inverted:
            subprocess.run(["taskkill", "/IM", "sakasa.exe", "/F"])
        is_there_quest, quest_type = self.is_there_question_type("post")
        if is_there_quest:
            questions_window = QuestionsWindow(master=self.root, trial_num=self.trial_counter, timing="post", quest_type=quest_type)
            self.root.wait_window(questions_window.window)  # blocks until questions_window is closed
        self.trial_counter += 1
        self.seconds_elapsed = 0
        self.time_in_target = 0
        self.global_update()

    def global_update(self):
        self.new_trial()
        if self.trial_counter < self.NumTrials:
            if self.trial_counter > 0 and self.trial_counter < self.NumTrials:
                self.lbl_transition = tk.Label(self.canvas, text="moving to the next trial",
                font=("Arial", 24), bg="blue",  fg="white", width=self.canvas.winfo_screenwidth(), height=3)
            else:
                self.lbl_transition = tk.Label(self.canvas, text="Welcome!",
                font=("Arial", 24), bg="blue",  fg="white", width=self.canvas.winfo_screenwidth(), height=3)
            self.lbl_transition.pack(anchor="n", fill="x")
            # brief pause between trials
            self.root.after(self.InterTrialTime, lambda: self.pre_trial_questions_and_start()) 
        else:
            self.lbl_transition = tk.Label(self.canvas, text="Congratulations! You have completed all of the trials",
            font=("Arial", 24), bg="blue",  fg="white", width=self.canvas.winfo_screenwidth(), height=3)
            self.lbl_transition.pack(anchor="n", fill="x")
            self.root.after(5000, lambda: self.restart_window())

    def trial_update(self):
        self.seconds_elapsed += 0.1
        # self.lbl_timer.config(text=str(int(self.seconds_elapsed)))
        if np.allclose(self.seconds_elapsed, self.PreparationTime/1000):
            self.lbl_triangle.place(relx=0.5, rely=0.5, anchor='center') 
            self.lbl_triangle.config(image=self.img_triangle_preloaded)
            self.lbl_triangle.image = self.img_triangle_preloaded
        if np.allclose(self.seconds_elapsed, self.PreparationTime/1000 + self.TriangleTime/1000): 
            self.lbl_triangle.place_forget()
        if np.allclose(self.seconds_elapsed, self.PreparationTime/1000 + self.TriangleTime/1000 + self.TriangleTargetInterval[self.trial_counter]/1000) and not self.target_set: # second part not necessary if allclose precise enough
            # unlock_cursor()
            self.lbl_decoy_target.config(image=self.img_target_preloaded)
            self.lbl_decoy_target.image = self.img_target_preloaded
            if self.Inverted: 
               # TODO add path to sakasa.exe
               subprocess.Popen(["C\\path\\to\\sakasa.exe"])
            if not self.MouseAppears[self.trial_counter]:
               self.root.config(cursor="none")
            self.show_target_based_on_pos()

        elif self.seconds_elapsed > 0: 
            self.root.after(100, lambda: self.trial_update())  

    def gen_csv_config_file(self): 
        np.random.seed(42)
        dir_path = os.path.dirname(os.path.abspath(__file__))
        config_dir = "Configurations"
        file_name = 'Re'
        FilePath = os.path.join(dir_path, config_dir, file_name)
        # 1) Target position (ratios set by D. Zarka)
        target_pos_key = [0, 1, 2] # left, center, right respectively 
        target_pos_probabilities = [0.45, 0.10, 0.45]
        target_pos = np.random.choice(target_pos_key, self.NumTrials, p=target_pos_probabilities)
        # 2) Mouse appears frequency
        mouse_appear_key = [0, 1]
        mouse_probabilities = [1-(self.MouseAppearFreq/100), self.MouseAppearFreq/100]
        mouse_appears = np.random.choice(mouse_appear_key, self.NumTrials, p=mouse_probabilities)
        # 3) Trigger Position
        trigger_pos = np.random.choice(self.TriggerPosVal, self.NumTrials)
        # 4) Triangle - Target delay 
        triangle_target_interval = np.random.choice(self.TriangleTargetIntervalVal, self.NumTrials)
        # zip function to group the ith elements together
        transposed_data = zip(target_pos, mouse_appears, trigger_pos, triangle_target_interval)
        with open(FilePath, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write each group of values as a row in the CSV file
            writer.writerows(transposed_data)

"""
def lock_cursor_to_rect(x, y, width, height):
    rect = RECT(x, y, x + width, y + height)
    user32.ClipCursor(ctypes.byref(rect))

def unlock_cursor():
    user32.ClipCursor(None)
"""