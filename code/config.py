import os
import zipfile
import shutil
import glob
import json
from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog


TEMP_PATH = os.path.join('.', 'temp')   # ./temp文件夹路径
DATA_PATH = os.path.join('.', 'data.json')  # ./data.json文件夹路径