import tkinter as tk
import tkinter.ttk as ttk

import os 
import json
from PIL import Image,ImageTk,ImageDraw
import pyautogui
import time
import numpy as np

from Config import *

class OpenFolderWindow: 
        def __init__(self, master):
           print("Lets dig inside of this folder")
