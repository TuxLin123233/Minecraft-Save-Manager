import os
import sys
import zipfile
import shutil
import glob
import json
from pathlib import Path
from tkinter import filedialog

from PIL import Image
import customtkinter as ctk


class PathConfig:
    """路径配置类，包含获取基础路径、字体路径和音频路径的方法"""
    def __init__(self) -> None:
        # 检查是否在PyInstaller打包环境中运行
        self.frozen: bool = getattr(sys, 'frozen', False)
        if self.frozen:
            self.temp_resource = Path(sys._MEIPASS)  # type: ignore

        # 获取基础路径(即以项目为开头)
        self.BASE_PATH = self.get_base_path()
        
        # === 项目资源文件夹 ===
        # 临时文件夹路径
        self.TEMP_PATH = self.BASE_PATH / 'temp'
        # 数据文件路径
        self.DATA_PATH = self.BASE_PATH / 'data.json'
        # 字体文件夹路径（仅用于开发环境）
        self.FONTS_PATH = self.BASE_PATH / 'fonts'

        # === 字体文件 ===
        # 字体文件名（用于加载文件）
        self.FONT_REGULAR_FILENAME = "HarmonyOS_Sans_SC_Regular.ttf"
        self.FONT_MEDIUM_FILENAME = "HarmonyOS_Sans_SC_Medium.ttf"
        # 字体系统名称（用于创建字体）
        self.FONT_REGULAR_NAME = "HarmonyOS Sans SC"           # 注意：有空格，没有下划线
        self.FONT_MEDIUM_NAME = "HarmonyOS Sans SC Medium"     # 注意：有空格，没有下划线
        # 字体文件路径
        self.FONT_REGULAR_PATH = self.get_font_path(self.FONT_REGULAR_FILENAME)
        self.FONT_MEDIUM_PATH = self.get_font_path(self.FONT_MEDIUM_FILENAME)
        
        # 音频文件夹路径
        self.SOUND_PATH = self.BASE_PATH / 'sounds'

    def get_base_path(self) -> Path:
        """获取基础路径，支持开发环境和打包环境

        Returns:
            Path: 基础路径对象
        """
        if self.frozen:
            # 打包环境：使用可执行文件所在目录
            return Path(sys.executable).parent
        else:
            # 开发环境：使用项目根目录
            return Path(__file__).parent.parent

    def get_font_path(self, font_name: str) -> Path:
        """获取字体文件完整路径

        Args:
            font_name (str): 字体文件名称（含扩展名）

        Returns:
            Path: 字体文件的完整绝对路径
        """
        # 检查是否在PyInstaller打包环境中运行
        if self.frozen:
            # 打包环境
            return self.temp_resource / 'fonts' / font_name
        else:
            # 开发环境：使用项目根目录的fonts文件夹
            return self.FONTS_PATH / font_name

    def get_sound_path(self, sound_name:str) -> Path:
        """获取音频文件完整路径

        Args:
            sound_name (str): 音频文件名(含扩展名)
        Returns:
            Path: 音频文件的完整绝对路径
        """
        if self.frozen:
            # 打包环境
            return self.temp_resource / 'sounds' / sound_name
        else:
            # 开发环境
            return self.SOUND_PATH / sound_name

# 创建路径配置实例
path_config = PathConfig()