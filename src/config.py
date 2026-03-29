import os
import sys
import zipfile
import shutil
import glob
import json
from pathlib import Path
from tkinter import filedialog
from playsound3 import playsound

from PIL import Image
import customtkinter as ctk


class PathConfig:
    """路径配置类，包含获取基础路径、字体路径和音频路径的方法
    
    逻辑流程:
        初始化实例
        ↓
        检测是否为 PyInstaller 打包环境
        ↓
        获取基础路径
        ↓
        配置各资源文件夹路径 (temp, data, fonts, sounds)
        ↓
        配置字体文件路径和名称
        ↓
        配置音频文件路径
    """
    def __init__(self) -> None:
        """初始化路径配置
        
        逻辑流程:
            检查是否在PyInstaller打包环境中运行
            ↓
            如果是打包环境，获取临时资源路径
            ↓
            获取基础路径
            ↓
            设置各资源文件夹路径
            ↓
            设置字体文件和名称
            ↓
            设置音频文件夹路径
            
        Returns:
            None
        """
        self.frozen: bool = getattr(sys, "frozen", False)
        if self.frozen:
            self.temp_resource: Path = Path(sys._MEIPASS)     # type:ignore

        self.BASE_PATH: Path = self.get_base_path()
        
        self.TEMP_PATH: Path = self.BASE_PATH / "temp"
        self.DATA_PATH: Path = self.BASE_PATH / "data.json"
        self.FONTS_PATH: Path = self.BASE_PATH / "fonts"

        self.FONT_REGULAR_FILENAME: str = "HarmonyOS_Sans_SC_Regular.ttf"
        self.FONT_MEDIUM_FILENAME: str = "HarmonyOS_Sans_SC_Medium.ttf"
        self.FONT_REGULAR_NAME: str = "HarmonyOS Sans SC"
        self.FONT_MEDIUM_NAME: str = "HarmonyOS Sans SC Medium"
        self.FONT_REGULAR_PATH: Path = self.get_font_path(self.FONT_REGULAR_FILENAME)
        self.FONT_MEDIUM_PATH: Path = self.get_font_path(self.FONT_MEDIUM_FILENAME)
        
        self.SOUND_PATH: Path = self.BASE_PATH / "sounds"

    def get_base_path(self) -> Path:
        """获取基础路径，支持开发环境和打包环境

        逻辑流程:
            判断是否为打包环境
            ├─ 打包环境: 返回可执行文件所在目录
            └─ 开发环境: 返回项目根目录 (__file__ 的父目录的父目录)

        Returns:
            Path: 基础路径对象
        """
        if self.frozen:
            return Path(sys.executable).parent
        else:
            return Path(__file__).parent.parent

    def get_font_path(self, font_name: str) -> Path:
        """获取字体文件完整路径

        逻辑流程:
            判断是否为打包环境
            ├─ 打包环境: 返回临时资源目录下的字体文件路径
            └─ 开发环境: 返回项目 fonts 文件夹下的字体文件路径

        Args:
            font_name (str): 字体文件名称（含扩展名）

        Returns:
            Path: 字体文件的完整绝对路径
        """
        if self.frozen:
            return self.temp_resource / "fonts" / font_name
        else:
            return self.FONTS_PATH / font_name

    def get_sound_path(self, sound_name: str) -> Path:
        """获取音频文件完整路径

        逻辑流程:
            判断是否为打包环境
            ├─ 打包环境: 返回临时资源目录下的音频文件路径
            └─ 开发环境: 返回项目 sounds 文件夹下的音频文件路径

        Args:
            sound_name (str): 音频文件名(含扩展名)
        Returns:
            Path: 音频文件的完整绝对路径
        """
        if self.frozen:
            return self.temp_resource / "sounds" / sound_name
        else:
            return self.SOUND_PATH / sound_name


path_config = PathConfig()

data_defalut = {"minecraft_path": "", "migrate": False}
