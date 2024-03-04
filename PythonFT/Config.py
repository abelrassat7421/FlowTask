import json
import csv
import tkinter as tk
from tkinter import messagebox

class Config:
    def __init__(self, json_file, master):
        with open(json_file, 'r') as file:
            data = json.load(file)
            
            self.root = master
            self.num_questions = data["num_questions"]
            self.questions = data["questions"]
            self.inverted = data["inverted"]
            self.trigger_visible = data["trigger_visible"]
            self.configure_with_csv = data["configure_with_csv"]
            self.direction_triangles = data["direction_triangles"]
            if not self.configure_with_csv:
                self.mouse_appear_freq = data["mouse_appear_freq"]
                self.num_triggers = data["num_triggers"]
                self.trigger_values = [val for val in data["trigger_values"]] 
                self.num_triangle_target_interval = data["num_triangle_target_interval"]
                self.time_intervals = data["time_intervals"]
                if self.direction_triangles:
                    self.freq_false_directions = data["freq_false_directions"]
            self.trajectory_sampling_rate = data["trajectory_sampling_rate"]
            self.inter_trial_time = data["inter-trial_time"]
            self.preparation_time = data["preparation_time"]
            self.time_to_center_of_target = data["time_to_center_of_target"]
            self.triangle_time = data["triangle_time"]
            self.num_random_trial = data["num_random_trial"]            
            self.target_size = data["target_size"]

    def read_config(self, gen_config_file): 
        # Lists to hold the data
        self.target_pos = []
        self.mouse_appears = []
        self.trigger_pos = []
        self.triangle_target_interval = []
        self.triangle_direction = []

        # Open the CSV file for reading
        with open(gen_config_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                self.target_pos.append(int(row[0]))
                self.mouse_appears.append(int(row[1]))
                self.trigger_pos.append(int(float(row[2])))
                self.triangle_target_interval.append(int(row[3]))
                if self.direction_triangles:
                   self.triangle_direction.append(int(row[4]))

            # testing if the values are acceptable
            N = self.num_random_trial
        
            general_error_mess = "\n\nPlease restart the application and modify the values in trial_by_trial_config.csv or populate the file from the application's settings window"
            try:
                if N != len(self.target_pos) or N != len(self.mouse_appears) or N != len(self.trigger_pos) or N != len(self.triangle_target_interval):
                    raise ValueError("The number of complete rows in trial_by_trial_config.csv must match the number of random trials (to be changed in settings)")
                elif not all(x in [0, 1, 2] for x in self.target_pos):
                    raise ValueError("Values in the first column of the trial_by_trial_config.csv file must be between either 0, 1 or 2 (respectively target appearing on the left, center and on the right)")
                elif not all(x in [0, 1] for x in self.mouse_appears):
                    raise ValueError("Values in the second column of the trial_by_trial_config.csv file must be either 0 or 1 (whether the mouse appears or not)")
                elif not all(x >= 0 or x <= 100 for x in self.trigger_pos):
                    raise ValueError("Values in the third column of the trial_by_trial_config.csv file must be between 0 and 100 (percentage where 0% is the bottom of the screen and 100% the top)")
                elif self.direction_triangles and N != len(self.triangle_direction):
                    raise ValueError("The fifth column of the trial_by_trial_config.csv file must be filled. Values must be set to 0, 1, 2 as for target position. If the values of the fifth column match those of the first column, there will be no false directions given.")
                
            except ValueError as e:
                response = messagebox.showwarning("Error", str(e) + general_error_mess)
                if response == 'ok':
                   self.root.destroy()
        if self.direction_triangles: 
            return self.target_pos, self.mouse_appears, self.trigger_pos, self.triangle_target_interval, self.triangle_direction
        else:
            return self.target_pos, self.mouse_appears, self.trigger_pos, self.triangle_target_interval

    """
    # Optional: Method to display the configuration
    def display(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
    """

