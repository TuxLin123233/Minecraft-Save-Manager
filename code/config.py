import os
import zipfile
import shutil
import glob
import json
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_PATH = os.path.join(BASE_DIR, "temp")  # ./temp文件夹路径
DATA_PATH = os.path.join(BASE_DIR, "data.json")  # ./data.json文件夹路径
