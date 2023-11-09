import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
import time
import numpy as np

from Config import *

class QuestionsWindow: 
    def __init__(self, master, trial_num, timing, quest_type, start_time):
        # here we assume that there exists at least one question with the given timing (checked for in Start.py)
        self.root = master
        self.trial_num = trial_num
        self.window = tk.Toplevel(master)
        self.window.title(f'Questions {timing}-trial')
        #self.window.focus_set() # Window Implemetation
        #self.window.attributes('-fullscreen', True)
        self.config = Config(master.ConfigFilePath, self.root) 
        self.Questions = quest_type
        self.num_questions = len(self.Questions)
        self.valid_key_pressed = False
        self.question_tracker = 0
        self.number_string = '123456789' 
        self.timing = timing
        self.quest_answers = []
        self.start_time = start_time
            
        # The answers to the quesitons will be saved in a txt file with format
        # pre_trial_questions_{nn} or post_trial_questions_{nn}
        self.frm_questions = ttk.Frame(self.window, borderwidth=2, relief="ridge")
        self.frm_questions.pack(expand=True, anchor='center')
        
        self.window.config(cursor="none")

        # Bind key press event
        self.window.bind("<Key>", self.on_key_press)

        # Bind the Escape key to toggle fullscreen mode
        self.window.bind("<Escape>", self.toggle_fullscreen)

        # Bind mouse events to disable them
        for mouse_event in ["<Button-1>", "<Button-2>", "<Button-3>", "<Double-Button-1>", "<B1-Motion>", "<Enter>", "<Leave>", "<MouseWheel>"]:
            self.window.bind(mouse_event, self.disable_mouse)

        # go through all questions with the given timing
        self.pass_through_questions(self.Questions[self.question_tracker])

    def pass_through_questions(self, quest):
        self.question_tracker += 1
        lbl_quest = tk.Label(master=self.frm_questions, text=f"Question {self.question_tracker}: " + quest["formulation"])
        lbl_quest.grid(row=0, column=0, pady=2, sticky='w')

        self.lbl_answer = tk.Label(master=self.frm_questions, text="0", bg="blue",  fg="white")
        self.lbl_answer.grid(row=0, column=1, pady=2, padx=10, sticky='w')

        self.lbl_guidelines = tk.Label(master=self.frm_questions, text=f"(Choisissez un nombre de 1 à {quest['answer_range']} sur le clavier)", font=("Arial", 8, "italic"))
        self.lbl_guidelines.grid(row=0, column=2 , padx=20, sticky='w')
        self.wait_move_to_next_question()
            
    def wait_move_to_next_question(self):
        if self.valid_key_pressed == True:
            self.clear_window_for_next_questions(self.timing)
            if self.question_tracker < self.num_questions:
               self.pass_through_questions(self.Questions[self.question_tracker])
        else:
            self.root.after(2000, lambda: self.wait_move_to_next_question())

    def on_key_press(self, event):
        # Check if key pressed is between 1 and 9 and if it's the first valid key press
        answer_range = self.Questions[self.question_tracker-1]["answer_range"]
        if event.char in self.number_string[:answer_range] and not self.valid_key_pressed:
            self.lbl_answer.config(text=str(int(event.char)))
            self.quest_answers.append(int(event.char))
            self.valid_key_pressed = True
        return "break" # Prevent further processing of the key event

    def disable_mouse(self, event):
        """Disable mouse events."""
        return "break"

    def clear_window_for_next_questions(self, timing):
        # check if all questions were asked
        if self.question_tracker == self.num_questions:
            self.save_answers(timing)
            self.window.destroy()
        else:
            for widget in self.frm_questions.winfo_children():
                widget.destroy()
        self.valid_key_pressed = False

    def save_answers(self, timing):
        # Read the existing JSON data
        dir_path = os.path.dirname(os.path.abspath(__file__))
        output_dir = 'Output'
        dir_current_output = f"Output_{self.start_time}"
        answer_dir = 'Answers'
        num = str(self.trial_num+1).zfill(2)
        file_name = f"{timing}_trial_questions_{num}"
        FilePath = os.path.join(dir_path, output_dir, dir_current_output, answer_dir, file_name)
        os.makedirs(os.path.dirname(FilePath), exist_ok=True)

        with open(FilePath, 'w') as file:
            # Gather user input for pre trial questions
            for i, quest in enumerate(self.quest_answers):
               file.write(f'Question {i+1}: Answer {quest}, (Formulation: {self.Questions[i]["formulation"]}, Answer Range: 1 to {self.Questions[i]["answer_range"]})\n')

    def toggle_fullscreen(self, event=None):
        state = not self.window.attributes('-fullscreen')  
        self.window.attributes('-fullscreen', state)
        return "break"





