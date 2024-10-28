# Script to generate the superposition of trajectories 
# from the mouse_trajectory_coord_num_csv files
# It will loop across all Output subfolders in the 
# main output directory

# TODO: convert this script into a function

import os 
import shutil
from PIL import Image,ImageTk,ImageDraw
import pyautogui
pyautogui.FAILSAFE = False
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import sys
import datetime
import colorsys
import glob
import re
from Config import *
from collections import Counter

# Check if the parent directory exists
dir_path = os.path.dirname(os.path.abspath(__file__))
config_dir = "Configurations"
dir_output = "Output"
Image_dir = "Images"
target_file_name = "target2.png"
cross_file_name = "cross.png"
config_file_name = "config.json"
ConfigFilePath = os.path.join(dir_path, config_dir, config_file_name)

TargetFilePath = os.path.join(dir_path, config_dir, Image_dir, target_file_name)
CrossFilePath = os.path.join(dir_path, config_dir, Image_dir, cross_file_name)
OutputPath = os.path.join(dir_path, dir_output)

# Load Config and images
config = Config(ConfigFilePath)
CrossSize = 20 # same as in Start.py
TargetSize = config.target_size
TrajSamplingRate = config.trajectory_sampling_rate
screen_width, screen_height = pyautogui.size()
print(f"Screen resolution: {screen_width} x {screen_height}")
image_tar = Image.open(TargetFilePath).convert("RGBA")
image_cross = Image.open(CrossFilePath).convert("RGBA")
image_tar_resized = image_tar.resize((TargetSize, TargetSize))
image_cross_resized = image_cross.resize((CrossSize, CrossSize))

# Define the colormaps for the trajectories based on velocities
colormap_name = 'winter' # # other sequential colormaps are the other season names or 'cool'
# reverse the colormap to have the lowest velocity in green
cmap_velocity = plt.get_cmap(colormap_name).reversed()
scaling_factor = 0.1 # same as in Start.py
max_velocity = np.sqrt(screen_width**2 + screen_height**2)/TrajSamplingRate * scaling_factor # assuming it's the diagonal of the screen traversed at the recording rate

if not os.path.exists(OutputPath):
    print(f"The directory '{OutputPath}' does not exist.")

# Iterate over items in the Output directory
for subfolder in os.listdir(OutputPath):
    subfolder_path = os.path.join(OutputPath, subfolder)
    
    if os.path.isdir(subfolder_path) and subfolder.startswith("Output_"):
        print(f"Processing folder trajectories from: {subfolder}")

        # open Trajectories folder in subfolder
        dir_trajectories = "Trajectories"
        TrajectoriesPath = os.path.join(subfolder_path, dir_trajectories)
        trial_by_trial_config = os.path.join(subfolder_path, 'trial_by_trial_config.csv')
        TargetPos = []
        with open(trial_by_trial_config, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                position = [int(val) for val in row[0].split(',')]
                TargetPos.append(position[0])

        # Define the colormaps for the trajectories based on velocities
        colormap_name = 'jet' #'spring'  
        cmap = plt.get_cmap(colormap_name)
        target_pos_counts = Counter(TargetPos)
        # find maximum occurence 
        max_occurence = max(target_pos_counts.values())
        intervals = np.linspace(0, 1, max_occurence) 
        colors = [cmap(interval) for interval in intervals]
        hex_colors_trial = [mcolors.to_hex(color) for color in colors] 

        # list to for aggregated trajectories by trial to have to have separate increments in colors for 
        # different target directions 
        occurrences = {0: 0, 1: 0, 2: 0}
        agg_traject_idx = []
        for num in TargetPos:
            agg_traject_idx.append(occurrences[num])
            occurrences[num] += 1 
        
        # Define the pattern for files with the required naming convention
        file_coord_pattern = os.path.join(TrajectoriesPath, "mouse_trajectory_coord_[0-9][0-9][0-9].csv")
        # Use glob to find all files that match the pattern
        file_coord_paths = glob.glob(file_coord_pattern)
        sorted_file_paths = sorted(file_coord_paths, key=lambda x: int(re.search(r'(\d{3})', os.path.basename(x)).group(1)))

        # create new Image objects to aggregate the trajectories
        agg_trial_image = Image.new("RGB", (screen_width, screen_height), "white")
        agg_velocity_image = Image.new("RGB", (screen_width, screen_height), "white")
        agg_trial_draw = ImageDraw.Draw(agg_trial_image)
        agg_velocity_draw = ImageDraw.Draw(agg_velocity_image)

        # Paste the target and cross images onto the Image object
        with open("lbl_target_winfo_y.txt", "r") as file:
                lbl_target_winfo_y = file.read().strip()
                lbl_target_winfo_y = int(lbl_target_winfo_y)  # Convert to int if needed
        _, _, _, a = image_tar_resized.split()
        agg_trial_image.paste(image_tar_resized, (round(screen_width*0.15 - 0.5*TargetSize), round(lbl_target_winfo_y)), mask=a)
        agg_trial_image.paste(image_tar_resized, (round(screen_width*0.5 - 0.5*TargetSize), round(lbl_target_winfo_y)), mask=a)
        agg_trial_image.paste(image_tar_resized, (round(screen_width*0.85 - 0.5*TargetSize), round(lbl_target_winfo_y)), mask=a)
        _, _, _, a = image_cross_resized.split()
        agg_trial_image.paste(image_cross_resized, (round(screen_width*0.5 - 0.5*CrossSize), round(0.95*screen_height - 0.5*CrossSize)), mask=a)

        _, _, _, a = image_tar_resized.split()
        agg_velocity_image.paste(image_tar_resized, (round(screen_width*0.15 - 0.5*TargetSize), round(lbl_target_winfo_y)), mask=a)
        agg_velocity_image.paste(image_tar_resized, (round(screen_width*0.5 - 0.5*TargetSize), round(lbl_target_winfo_y)), mask=a)
        agg_velocity_image.paste(image_tar_resized, (round(screen_width*0.85 - 0.5*TargetSize), round(lbl_target_winfo_y)), mask=a)
        _, _, _, a = image_cross_resized.split()
        agg_velocity_image.paste(image_cross_resized, (round(screen_width*0.5 - 0.5*CrossSize), round(0.95*screen_height - 0.5*CrossSize)), mask=a)        

        for file_id, file_coord in enumerate(sorted_file_paths):
            print("Processing file: ", file_coord)

            # Read the file 
            data_coord = np.loadtxt(file_coord, delimiter=';', skiprows=1)  # skip the header
            for i in range(1, data_coord.shape[0]):
                x1, y1 = data_coord[i-1]
                x2, y2 = data_coord[i]
                # trial 
                agg_trial_draw.line([(x1, y1), (x2, y2)], fill=hex_colors_trial[agg_traject_idx[file_id]], width=2)

                # velocity
                mouse_velocity = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)/TrajSamplingRate
                color_num = np.log(mouse_velocity + 1)/np.log(max_velocity + 1)
                color = cmap_velocity(color_num)
                agg_velocity_draw.line([(x1, y1), (x2, y2)], fill=mcolors.to_hex(color), width=2)

        # Save the aggregated trajectory image in the corresponding Trajectory file
        num = file_id + 1
        traj_file_name_agg_trial = f"post_hoc_mouse_trajectory_trial_agg_{num}.png"
        traj_file_path_agg_veloc = f"post_hoc_mouse_trajectory_velocity_agg_{num}.png"
        TrajFilePathTrialAgg = os.path.join(dir_path, dir_output, subfolder, dir_trajectories, traj_file_name_agg_trial)
        TrajFilePathVelocityAgg = os.path.join(dir_path, dir_output, subfolder, dir_trajectories,  traj_file_path_agg_veloc)
        agg_trial_image.save(TrajFilePathTrialAgg)
        agg_velocity_image.save(TrajFilePathVelocityAgg)

            


