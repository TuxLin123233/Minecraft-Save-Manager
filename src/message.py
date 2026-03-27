from config import *
from utils import *

class Message:
    """消息对话框类，提供信息提示框和是/否选择框
    
    逻辑流程:
        初始化 Message 实例
        ↓
        创建 Toplevel 窗口
        ↓
        设置窗口属性 (颜色、置顶)
        ↓
        初始化结果变量
        ↓
        配置按钮样式
    """
    def __init__(self, parent_window:ctk.CTk) -> None:
        """初始化消息对话框
        
        逻辑流程:
            创建子窗口
            ↓
            设置窗口背景色
            ↓
            设置窗口置顶父窗口
            ↓
            初始化结果变量为 False
            ↓
            配置按钮默认样式

        Args:
            parent_window: 父窗口对象

        Returns:
            None
        """
        self.window = ctk.CTkToplevel(parent_window)
        self.window.configure(fg_color="#D3D3D3")
        
        self.window.transient(parent_window)
        
        self.result = False
        
        self.btn_config = {
            "width": 90,
            "height": 40,
            "anchor": "center",
            "border_width": 2,
            "border_color": "#CFCFCF",
            "corner_radius": 13,
        }
    
    def on_confirm(self, value:bool=False):
        """确认按钮回调函数
        
        逻辑流程:
            保存用户选择的结果值
            ↓
            销毁窗口

        Args:
            value: 用户选择的值 (True 或 False)

        Returns:
            None
        """
        self.result = value
        self.window.destroy()
    
    def info(self, title:str, text:str, font:ctk.CTkFont):
        """消息通知框
        
        逻辑流程:
            设置窗口标题
            ↓
            播放信息提示音效
            ↓
            创建文本 Label
            ↓
            创建确定按钮
            ↓
            自动调整窗口宽度
            ↓
            窗口居中
            ↓
            设置为模态窗口
            ↓
            等待窗口关闭
            ↓
            返回用户选择结果

        Args:
            title: 对话框标题
            text: 显示的文本内容
            font: 使用的字体对象

        Returns:
            bool: 用户选择的结果
        """
        self.window.title(title)
        
        playsound(path_config.get_sound_path("message_info.mp3"), block=False)
        
        content = ctk.CTkLabel(
            self.window,
            text=text,
            font=font
        )
        content.pack(pady=(5, 0))
        
        confirm_button = ctk.CTkButton(
            self.window,
            text="确定",
            font=font,
            fg_color="#5E5E5E",
            hover_color="#505050",
            command=lambda:self.on_confirm(True), 
            **self.btn_config
        )
        confirm_button.pack(pady=(10, 0))
        
        auto_label_window_width(content, self.window, 95)
        center_window(self.window)
        
        self.window.grab_set()
        
        self.window.wait_window()
        
        return self.result

    def yes_no(self, title:str, text:str, font:ctk.CTkFont):
        """选择框
        
        逻辑流程:
            设置窗口标题
            ↓
            播放选择提示音效
            ↓
            创建文本 Label
            ↓
            创建按钮容器
            ↓
            创建"好的"按钮 (返回 True)
            ↓
            创建"不要"按钮 (返回 False)
            ↓
            自动调整窗口宽度
            ↓
            窗口居中
            ↓
            设置为模态窗口
            ↓
            等待窗口关闭
            ↓
            返回用户选择结果

        Args:
            title: 对话框标题
            text: 显示的文本内容
            font: 使用的字体对象

        Returns:
            bool: 用户选择的结果
        """
        self.window.title(title)
        
        playsound(path_config.get_sound_path("message_yes_no.mp3"), block=False)
        
        content = ctk.CTkLabel(
            self.window,
            text=text, 
            font=font
        )
        content.pack(pady=(5, 0))
        
        btn_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )
        btn_frame.pack(pady=(10, 0))
        
        yes_button = ctk.CTkButton(
            btn_frame,
            text="好的",
            fg_color="#86aa19",
            hover_color="#799b16",
            command=lambda:self.on_confirm(True),
            **self.btn_config
        )
        no_button = ctk.CTkButton(
            btn_frame,
            text="不要",
            command=lambda:self.on_confirm(False),
            **self.btn_config
        )
        yes_button.pack(side="left", padx=(0, 15))
        no_button.pack(side="left")
        
        auto_label_window_width(content, self.window, 95)
        center_window(self.window)
        
        self.window.grab_set()
        self.window.wait_window()
        
        return self.result
