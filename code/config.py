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
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # 项目根目录
TEMP_PATH = os.path.join(BASE_DIR, "temp")  # ./temp文件夹路径
DATA_PATH = os.path.join(BASE_DIR, "data.json")  # ./data.json文件夹路径
IMG_PATH = os.path.join(PROJECT_ROOT, "img")  # 项目根目录下的img文件夹路径
