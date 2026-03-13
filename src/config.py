import os
import sys
import zipfile
import shutil
import glob
import json
from tkinter import messagebox, filedialog

from PIL import Image
import customtkinter as ctk


def get_base_path():
    """获取基础路径，支持开发环境和打包环境

    Returns:
        str: 基础路径字符串，开发环境返回项目根目录，打包环境返回可执行文件所在目录
    """
    if getattr(sys, 'frozen', False):
        # 打包环境：使用可执行文件所在目录
        return os.path.dirname(sys.executable)
    else:
        # 开发环境：使用项目根目录
        return os.path.dirname(os.path.dirname(__file__))

def get_font_path(font_name):
    """获取字体文件完整路径

    Args:
        font_name (str): 字体文件名称（含扩展名）

    Returns:
        str: 字体文件的完整绝对路径
    """
    # 检查是否在PyInstaller打包环境中运行
    if getattr(sys, 'frozen', False):
        # 打包环境：使用sys._MEIPASS获取临时解压目录
        base_path = sys._MEIPASS # type: ignore
        return os.path.join(base_path, 'fonts', font_name)
    else:
        # 开发环境：使用项目根目录的fonts文件夹
        return os.path.join(FONTS_PATH, font_name)

# 获取基础路径(即以项目为开头)
BASE_PATH = get_base_path()

# 临时文件夹路径
TEMP_PATH = os.path.join(BASE_PATH, 'temp')

# 数据文件路径
DATA_PATH = os.path.join(BASE_PATH, 'data.json')

# 字体文件夹路径（仅用于开发环境）
FONTS_PATH = os.path.join(BASE_PATH, 'fonts')

# 字体文件名
FONT_REGULAR_NAME = "HarmonyOS_Sans_SC_Regular"
FONT_MEDIUM_NAME = "HarmonyOS_Sans_SC_Medium"

# 字体文件路径
FONT_REGULAR_PATH = get_font_path(f"{FONT_REGULAR_NAME}.ttf")
FONT_MEDIUM_PATH = get_font_path(f"{FONT_MEDIUM_NAME}.ttf")