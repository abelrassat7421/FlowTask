import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
pyautogui.FAILSAFE = False
import time
import numpy as np
#from LptPort import LptPort 

from Config import *

class QuestionsWindow: 
    def __init__(self, master, trial_num, timing, quest_type, start_time):
        # at least one question with the given timing exists (checked for in Start.py)
        self.root = master
        self.trial_num = trial_num
        self.window = tk.Toplevel(master)
        self.window.title(f'Questions {timing}-trial')
        self.window.focus_set() # Windows Implemetation

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
            
        # The answers to the questions will be saved in a txt file with format
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

        # try: 
        #     self.lptPort = LptPort(0x0378)   # Idea: should add the '0x0378' and other std LPT adresses in settings pannel
        # except:
        #     print("WARNING: LPT port NOT opened!")

        # go through all questions with the given timing
        self.pass_through_questions(self.Questions[self.question_tracker])

    def pass_through_questions(self, quest):
        self.question_tracker += 1
        lbl_quest = tk.Label(master=self.frm_questions, text=f"Question {self.question_tracker}: " + quest["formulation"], font=("Arial", 20))
        lbl_quest.grid(row=0, column=0, pady=2, sticky='w')

        self.lbl_answer = tk.Label(master=self.frm_questions, text="0", bg="blue",  fg="white", font=("Arial", 20))
        self.lbl_answer.grid(row=0, column=1, pady=2, padx=10, sticky='w')

        self.lbl_guidelines = tk.Label(master=self.frm_questions, text=f"(Select a number between 1 and {quest['answer_range']} on your keyboard)", font=("Arial", 12, "italic"))
        self.lbl_guidelines.grid(row=0, column=2 , padx=20, sticky='w')
        # if self.timing == "pre":
        #     self.lptPort.sendEvent(self.question_tracker*10)
        # if self.timing == "post":
        #     self.lptPort.sendEvent(self.question_tracker*10 + 100)

        self.wait_move_to_next_question()

            
    def wait_move_to_next_question(self):
        if self.valid_key_pressed == True:
            answer = self.quest_answers[-1]
            event_num = (self.question_tracker)*10 + answer
            # if self.timing == "pre":
            #    self.lptPort.sendEvent(event_num)
            # if self.timing == "post":
            #    self.lptPort.sendEvent(event_num+100)
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





