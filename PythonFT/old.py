# explicitly define to use classic or themed widgets
import tkinter as tk
# for themed widgets more modern looking
import tkinter.ttk as ttk
import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
import time
import numpy as np
"""
# override the classic widgets with the themed ones whenever possible
# better to remove wildcard import for the final version - good to start to gain time 
from tkinter import *
from tkinter.ttk import *
"""

# function that depend on the root - look into moving these to seperate file later on
def toggle_fullscreen(event=None):
    state = not root.attributes('-fullscreen')  
    root.attributes('-fullscreen', state)
    return "break"

def clear_window():
    # Destroy each child widget in the main window
    for widget in root.winfo_children():
        widget.destroy()

def draw_line(canvas, event=None):
    # Clear the canvas
    canvas.delete("all")
    root.update_idletasks()
    # Draw a horizontal line at 2/3 of the canvas height
    canvas.create_line(0, canvas.winfo_height() * 2/3, canvas.winfo_width(), canvas.winfo_height() * 2/3, fill="black", dash=(10))

def invert_mouse(event):
    global last_x
    if last_x is None:
        last_x = event.x
        return
    # Calculate the difference in x movement
    dx = event.x - last_x
    # Move the mouse to the inverted x position
    pyautogui.move(-2*dx, 0)  # Multiply by 2 because we want to counteract the user's movement and then apply the inverted movement
    # Update the last x position
    last_x = event.x

def capture_trajectory(traject_num, duration=5, sampling_rate=20):
    traj_file_name = f"mouse_trajectory_{traject_num}.png"
    dir_path = os.path.dirname(os.path.abspath(__file__))
    TrajFilePath = os.path.join(dir_path, traj_file_name)

    # Create a blank white image with the screen's dimensions
    img = Image.new("RGB", (screen_width, screen_height), "white")
    draw = ImageDraw.Draw(img)
    interval = 1.0 / sampling_rate

    # Store initial time
    start_time = time.time()
    # Store the previous position to draw a line between points
    prev_x, prev_y = pyautogui.position()

    while time.time() - start_time < duration:
        time.sleep(interval)
        # Get current mouse position
        x, y = pyautogui.position()
        # Draw a line from the previous position to the current position
        draw.line([(prev_x, prev_y), (x, y)], fill="black", width=2)
        # Update previous position
        prev_x, prev_y = x, y

    # Save the image as PNG
    img.save(TrajFilePath)
    print("Trajectory saved as mouse_trajectory.png")

def start_timer_based_on_mouse_position(seconds_el):
    # Get current mouse position
    x, y = pyautogui.position()
    # Check if the mouse is in the upper two-thirds of the screen
    if y < (2/3) * screen_height:
        update_timer(seconds_el)  # Start the timer with an initial value of 0 for seconds_elapsed
    else:
        # If not, schedule the function to check again after a short delay
        root.after(100, lambda: start_timer_based_on_mouse_position(seconds_el))

# Timer function
def update_timer(seconds_el):
    # When I'll be working with several trials use a timer in a similar fashion as what's done above
    global seconds_elapsed
    seconds_elapsed = seconds_el
    seconds_elapsed += 1
    inverted = CONFIG['inverted']

    # Update the timer label
    lbl_timer.config(text=str(seconds_elapsed))
    """
    print("DEBUG last_x: ", last_x)
    
    if seconds_elapsed == 5:
        if inverted: 
            root.bind('<Motion>', invert_mouse)
    if seconds_elapsed == 25:
        root.unbind('<Motion>')
    """
    """
    if seconds_elapsed == 5:
        lbl_triangle.config(image=img_triangle_preloaded)
        lbl_triangle.image = img_triangle_preloaded
    if seconds_elapsed == 7:
        # For now remove triangle 1 second before the target should popup
        lbl_triangle.pack_forget()
    if seconds_elapsed == 8:
        lbl_target.config(image=img_target_preloaded)
        lbl_target.image = img_target_preloaded
        if inverted: 
           root.bind('<Motion>', invert_mouse)
        capture_trajectory(traject_num=1)
    """

    root.after(1000, lambda: update_timer(seconds_elapsed))  # Schedule the function to run again after 1000 milliseconds

# Command functions called by various button widgets
def start():
    trigger_visible = CONFIG['trigger_visible']
    clear_window()

    # delay to allow the user to move the mouse to the lower 1/3 of the screen
    time.sleep(2)
    seconds_elapsed = 0

    # Create a canvas that spans the entire width of the window
    canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height(), bg="white")
    print(root.winfo_width(), root.winfo_height())
    print(canvas.winfo_width(), canvas.winfo_height())
    canvas.pack(fill=tk.BOTH, expand=True)

    # Set the black starting box
    frm_starting_block = tk.Frame(master=canvas, width=200, height=100, bg="#3E3C44")
    frm_starting_block.pack_propagate(0) # Prevent the frame from resizing to fit its contents

    # Position the frame at the bottom center of the canvas
    frm_starting_block.place(relx=0.5, rely=1, anchor='s')

    # Showing the trigger on the screen
    if trigger_visible: 
        # Draw the initial line
        draw_line(canvas)

    # Bind the resize event of the window to adjust the line's width
    # root.bind("<Configure>", draw_line)

    global lbl_target
    global lbl_triangle
    global lbl_timer

    # Label for images (initally empty)
    lbl_target = tk.Label(root)
    lbl_triangle = tk.Label(root)

    # the Target should stay centered relative to the window regardless of the window size
    lbl_target.pack(expand=True)
    lbl_triangle.pack(expand=True)

    ## DEBUGGING
    # Create a label for the timer
    lbl_timer = tk.Label(root, text="0")
    lbl_timer.place(relx=0.95, rely=0.95, anchor='se')  # Positioning the label in the lower right corner

    # The timer starts when the main window opens
    start_timer_based_on_mouse_position(seconds_elapsed)

def settings():
    # Save configuations 
    def save_settings():
        # Gather user input (for demonstration purposes, I'm assuming Checkbuttons for the questions)
        val_quest1 = clk_quest1.get()
        val_quest2 = clk_quest2.get()
        val_quest3 = clk_quest3.get()
        val_quest4 = clk_quest4.get()
        val_inverted = clk_inverted.get()
        val_trigger_visible = clk_trigger_visible.get()
        val_sec_to_center = ent_sec_to_center.get()
        val_prepare_time = ent_prepare_time.get()
        val_min_delay = ent_min_delay.get()
        val_max_delay = ent_max_delay.get()
        val_msgbox_bef_tar_min_time = ent_msgbox_bef_tar_min_time.get()
        val_msgbox_bef_tar_max_time = ent_msgbox_bef_tar_max_time.get()
        val_num_random_trial = ent_num_random_trial.get()
        val_center_trigger = ent_center_trigger.get()
        val_target_size = ent_target_size.get()

        # Read the existing JSON data
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_name = "config.json"
        FilePath = os.path.join(dir_path, file_name)
        with open(FilePath, 'r') as file:
            data = json.load(file)

        # Update the values
        data["question_1"] = val_quest1
        data["question_2"] = val_quest2
        data["question_3"] = val_quest3
        data["question_4"] = val_quest4
        data["inverted"] = val_inverted
        data["seconds_to_center_of_target"] = int(val_sec_to_center)
        data["prepare_time"] = int(val_prepare_time)
        data["min_delay"] = int(val_min_delay)
        data["max_delay"] = int(val_max_delay)
        data["msgbox_before_target_min_time"] = int(val_msgbox_bef_tar_min_time)
        data["msgbox_before_target_max_time"] = int(val_msgbox_bef_tar_max_time)
        data["num_random_trial"] = int(val_num_random_trial)
        data["center_trigger"] = int(val_center_trigger)
        data["target_size"] = int(val_target_size)
        data["trigger_visible"] = val_trigger_visible

        # Write the updated data back to the JSON file
        with open(FilePath, 'w') as file:
            json.dump(data, file, indent=4)

    # 1 DO: have the settings window open as a smaller window over the root window in fullscreen
    settings_window = tk.Toplevel()
    settings_window.title('Settings')
    # settings.iconbitmap('PythonFlowTask/target.ico') some settings/gear icon to add

    # 3 DO: change the size of the frame for interior padding (or padding on its widgets)
    frm_settings = ttk.Frame(settings_window, borderwidth=2, relief="ridge")
    frm_settings.pack(expand=True, anchor='nw')
        
    # Labels
    lbl_quest1 = tk.Label(master=frm_settings, text="Question 1:")
    lbl_quest2 = tk.Label(master=frm_settings, text="Question 2:")
    lbl_quest3 = tk.Label(master=frm_settings, text="Question 3:")
    lbl_quest4 = tk.Label(master=frm_settings, text="Question 4:")
    lbl_inverted = tk.Label(master=frm_settings, text="Is Inverted?:")
    lbl_sec_to_center = tk.Label(master=frm_settings, text="Seconds to Center of target:")
    lbl_prepare_time = tk.Label(master=frm_settings, text="Prapare time:")
    lbl_min_delay = tk.Label(master=frm_settings, text="Minimum Delay:")
    lbl_max_delay = tk.Label(master=frm_settings, text="Maximum Delay:")
    lbl_msgbox_bef_tar_min_time = tk.Label(master=frm_settings, text="Message Box before target minimum time:")
    lbl_msgbox_bef_tar_max_time = tk.Label(master=frm_settings, text="Message Box before target msximum time:")
    lbl_num_random_trial = tk.Label(master=frm_settings, text="Number of Random Trials:")
    lbl_center_trigger = tk.Label(master=frm_settings, text="Center trigger:")
    lbl_target_size = tk.Label(master=frm_settings, text="Target Size:")
    lbl_trigger_visible = tk.Label(master=frm_settings, text="Trigger Visible?:")
    # check if this was specific to the C# implementation
    # lbl_1ptPortAddress=800
    # lbl_1ptPortUpTime=5

    lbl_quest1.grid(row=0, column=0, pady=2, sticky='w')
    lbl_quest2.grid(row=1, column=0, pady=2, sticky='w')
    lbl_quest3.grid(row=2, column=0, pady=2, sticky='w')
    lbl_quest4.grid(row=3, column=0, pady=2, sticky='w')
    lbl_inverted.grid(row=4, column=0, pady=2, sticky='w')
    lbl_sec_to_center.grid(row=5, column=0, pady=2, sticky='w')
    lbl_prepare_time.grid(row=6, column=0, pady=2, sticky='w')
    lbl_min_delay.grid(row=7, column=0, pady=2, sticky='w')
    lbl_max_delay.grid(row=8, column=0, pady=2, sticky='w')
    lbl_msgbox_bef_tar_min_time.grid(row=9, column=0, pady=2, sticky='w')
    lbl_msgbox_bef_tar_max_time.grid(row=10, column=0, pady=2, sticky='w')
    lbl_num_random_trial.grid(row=11, column=0, pady=2, sticky='w')
    lbl_center_trigger.grid(row=12, column=0, pady=2, sticky='w')
    lbl_target_size.grid(row=13, column=0, pady=2, sticky='w')
    lbl_trigger_visible.grid(row=14, column=0, pady=2, sticky='w')

    # discrete set of options for dropdowns
    optionTF = [True, False]
    clk_quest1 = tk.BooleanVar()
    clk_quest2 = tk.BooleanVar()
    clk_quest3 = tk.BooleanVar()
    clk_quest4 = tk.BooleanVar()
    clk_inverted = tk.BooleanVar()
    clk_trigger_visible = tk.BooleanVar()
    clk_quest1.set(optionTF[0])
    clk_quest2.set(optionTF[0])
    clk_quest3.set(optionTF[0])
    clk_quest4.set(optionTF[0])
    clk_inverted.set(optionTF[1])
    clk_trigger_visible.set(optionTF[1])
 
    # default values (not those that are currently in the .json file)
    drp_quest1 = tk.OptionMenu(frm_settings, clk_quest1, *optionTF)
    drp_quest2 = tk.OptionMenu(frm_settings, clk_quest2, *optionTF)
    drp_quest3 = tk.OptionMenu(frm_settings, clk_quest3, *optionTF)
    drp_quest4 = tk.OptionMenu(frm_settings, clk_quest4, *optionTF)
    drp_inverted = tk.OptionMenu(frm_settings, clk_inverted, *optionTF) 
    drp_trigger_visible = tk.OptionMenu(frm_settings, clk_trigger_visible, *optionTF)
    ent_sec_to_center = ttk.Entry(frm_settings)
    ent_prepare_time = ttk.Entry(frm_settings)
    ent_min_delay = ttk.Entry(frm_settings)
    ent_max_delay = ttk.Entry(frm_settings)
    ent_msgbox_bef_tar_min_time = ttk.Entry(frm_settings)
    ent_msgbox_bef_tar_max_time = ttk.Entry(frm_settings)
    ent_num_random_trial = ttk.Entry(frm_settings)
    ent_center_trigger = ttk.Entry(frm_settings)
    ent_target_size = ttk.Entry(frm_settings)
    # Default Values already displayed
    ent_sec_to_center.insert(0, "2")
    ent_prepare_time.insert(0, "500")
    ent_min_delay.insert(0, "800")
    ent_max_delay.insert(0, "1200")
    ent_msgbox_bef_tar_min_time.insert(0, "500")
    ent_msgbox_bef_tar_max_time.insert(0, "1500")
    ent_num_random_trial.insert(0, "20")
    ent_center_trigger.insert(0, "20")
    ent_target_size.insert(0, "120")

    drp_quest1.grid(row=0, column=1, pady=2, padx=10, sticky='w')
    drp_quest2.grid(row=1, column=1, pady=2, padx=10, sticky='w')
    drp_quest3.grid(row=2, column=1, pady=2, padx=10, sticky='w')
    drp_quest4.grid(row=3, column=1, pady=2, padx=10, sticky='w')
    drp_inverted.grid(row=4, column=1, pady=2, padx=10, sticky='w')
    ent_sec_to_center.grid(row=5, column=1, pady=2, padx=10, sticky='w')
    ent_prepare_time.grid(row=6, column=1, pady=2, padx=10, sticky='w')
    ent_min_delay.grid(row=7, column=1, pady=2, padx=10, sticky='w')
    ent_max_delay.grid(row=8, column=1, pady=2, padx=10, sticky='w')
    ent_msgbox_bef_tar_min_time.grid(row=9, column=1, pady=2, padx=10, sticky='w')
    ent_msgbox_bef_tar_max_time.grid(row=10, column=1, pady=2, padx=10, sticky='w')
    ent_num_random_trial.grid(row=11, column=1, pady=2, padx=10, sticky='w')
    ent_center_trigger.grid(row=12, column=1, pady=2, padx=10, sticky='w')
    ent_target_size.grid(row=13, column=1, pady=2, padx=10, sticky='w')
    drp_trigger_visible.grid(row=14, column=1, pady=2, padx=10, sticky='w')

    btn_save = ttk.Button(frm_settings, text="Save", command=save_settings)
    btn_save.grid(row=15, column=0, pady=100, padx=20, sticky='sw')

def open_folder():
    print("Lets dig inside of this folder")

# get screen dimensions
"""
# Get screen width and height 
# for some reason these values are half of what I see in System Setting > General
# may need to always scale by a factor 2
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

widthLabel = Label(root, text="Window width: " + str(screen_width))
heightLabel = Label(root, text="Window height: " + str(screen_height))

widthLabel.grid(row=0, column=0)
heightLabel.grid(row=0, column=1)
"""

# Create main window 
root = tk.Tk()
root.title('Flow Task v1.0')
# root.iconbitmap('PythonFlowTask/target.ico')

# Bind the Escape key to toggle fullscreen mode
root.bind("<Escape>", toggle_fullscreen)

# screen attributes 
print(root.winfo_screenwidth()) # getting the scaled values in points, not the actual pixel resolution (factor x2 on Retina screen)
print(root.winfo_screenheight()) # method to get the actual number of pizels requires platform-specific approaches

# window attributes & size
# root.attributes("-topmost", True) # when window is open it will always be in front of any other existing window
root.attributes("-fullscreen", True) # need terminal or IDE from where program executed not in full screen
root.minsize(200, 100)
# root.overrideredirect(True) # removing the title bar 

# Probably change the names of these variables
dir_path = os.path.dirname(os.path.abspath(__file__))
target_file_name = "target.png"
TargetFilePath = os.path.join(dir_path, target_file_name)
triangle_file_name = "triangle.png"
TriangleFilePath = os.path.join(dir_path, triangle_file_name)
config_file_name = "config.json"
ConfigFilePath = os.path.join(dir_path, config_file_name)
with open(ConfigFilePath, 'r') as file:
    CONFIG = json.load(file)

# Preload and process images outside the update_timer function
screen_width, screen_height = pyautogui.size()
TargetWidth = CONFIG['target_size']
TargetHeight = CONFIG['target_size']
TriangleWidth = 100
TriangleHeight = 100
image_tar = Image.open(TargetFilePath)
image_tri = Image.open(TriangleFilePath)
image_tar_resized = image_tri.resize((TargetWidth, TargetHeight))
image_tri_resized = image_tri.resize((TriangleWidth, TriangleHeight))
img_target_preloaded = ImageTk.PhotoImage(image_tar_resized)
img_triangle_preloaded = ImageTk.PhotoImage(image_tri_resized)

# position initialisation when the inverted option is set to True
last_x = None

# Welcome window
frm_buttons = ttk.Frame(root)
frm_buttons.pack(expand=True, anchor='center')

max_width = max(len("Start"), len("Settings"), len("Open Folder"))

btn_start = ttk.Button(frm_buttons, text="Start", command=start, width=max_width)
btn_settings = ttk.Button(frm_buttons, text="Settings", command=settings, width=max_width)
button_open = ttk.Button(frm_buttons, text="Open Folder", command=open_folder, width=max_width)

btn_start.pack(pady=5)
btn_settings.pack(pady=5)
button_open.pack(pady=5)

# Run the Tkinter event loop - code that follows will only be ran once this window is closed
# Checks if any event has occurred 
root.mainloop()

# Event handlers for the events in the application



