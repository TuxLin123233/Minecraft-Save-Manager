from config import *
from utils import *


class App:
    def __init__(self):
        """GUI应用程序类初始化

        Returns:
            None
        """
        self.window = ctk.CTk()
        self.window.title("🗃 存档管理器")
        self.window.geometry("400x290")
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        ctk.set_appearance_mode("light")

        # 加载字体文件
        ctk.FontManager.load_font(FONT_REGULAR_PATH)
        ctk.FontManager.load_font(FONT_MEDIUM_PATH)
        
        # 设置组件字体
        self.font_button = ctk.CTkFont(family=FONT_MEDIUM_NAME, size=16)
        self.font_header = ctk.CTkFont(family=FONT_MEDIUM_NAME, size=24, weight="bold")
        self.font_label = ctk.CTkFont(family=FONT_REGULAR_NAME, size=14)
        
        self.create_header()    # 标题部分
        self.create_buttons()   # 按钮部分

    def create_header(self):
        """创建标题区域，显示应用名称和图标

        Returns:
            None
        """
        header_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        header_frame.pack(pady=20)

        steve_image = get_image('tool', size=(32, 32))
        image_label = ctk.CTkLabel(header_frame, image=steve_image, text="")
        image_label.pack(side='left', padx=(0, 5), pady=(5, 0))

        # 大标题
        title = ctk.CTkLabel(
            header_frame,
            text="Minecraft 存档管理器",
            font=self.font_header,
            text_color="#333333",
        )
        title.pack(side="left")

    def create_buttons(self):
        """创建功能按钮区域，包含导入存档、导出存档、存档列表、赞助一下四个按钮

        Returns:
            None
        """
        # 按钮容器
        btn_container = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_container.pack(expand=True, fill="both", padx=45)

        # 第一行容器
        row1 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row1.pack(fill="both")
        
        # 第二行容器
        row2 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row2.pack(fill="both", pady=(20, 0))

        # 按钮默认参数
        btn_config = {
            "width": 130,
            "height": 85,
            "font": self.font_button,
            "compound": "bottom",    # 文字在底部，图片在顶部
            "anchor": "center",      # 整体居中
            "border_width": 2,
            "border_color": "#CFCFCF",
            "corner_radius": 13,
        }
        
        
        # 第一行按钮：导入存档
        btn1 = ctk.CTkButton(
            row1,
            text="导入存档",
            command=self.import_save,
            fg_color="#2c4068",
            hover_color="#1d2f53",
            text_color="#cfdaf2",
            image=get_image('import', (26, 26)),
            **btn_config,
        )
        btn1.pack(side="left", padx=12)

        # 第一行按钮：导出存档
        btn2 = ctk.CTkButton(
            row1,
            text="导出存档",
            command=self.export_save,
            fg_color="#793231",
            hover_color="#682d2c",
            text_color="#FBE3E3",
            image=get_image('export', (30, 30)),
            **btn_config,
        )
        btn2.pack(side="left", padx=12)

        # 第二行按钮：存档列表
        btn3 = ctk.CTkButton(
            row2,
            text="存档列表",
            command=self.list_saves,
            fg_color="#795431",
            hover_color="#614021",
            text_color="#FFECDB",
            image=get_image('list', (30, 30)),
            **btn_config,
        )
        btn3.pack(side="left", padx=12)

        # 第二行按钮：赞助一下
        btn4 = ctk.CTkButton(
            row2,
            text="赞助一下",
            command=self.donate,
            fg_color="#6E9D28",
            hover_color="#5C861C",
            text_color="#F7FFEC",
            image=get_image('donate', (30, 30)),
            **btn_config,
        )
        btn4.pack(side="left", padx=12)

    def import_save(self):
        """导入存档功能，将ZIP格式的地图文件解压到Minecraft的saves文件夹

        Returns:
            None
        """
        # ====== 第一步：获取.minecraft路径 ======
        data = read_data()  # 获取数据文件
        minecraft_path = data['minecraft_path'] # 获取.minecraft文件夹

        # ====== 第二步：检查并确认.minecraft路径 ======
        # 检查用户是否已经保存过.minecraft文件夹路径
        if minecraft_path:  # 用户已记录minecraft文件夹路径
            # ====== 第三步：选择ZIP文件夹 ======
            zip_folder_path = folder_dialog("选择存放地图ZIP的文件夹")
            # 如果用户取消了文件夹选择，直接返回
            if not zip_folder_path:
                return
        else:  # 如果没有记录
            # 询问用户是否愿意提供.minecraft文件夹路径
            result = messagebox.askyesno(
                "温馨提示",
                "导入存档前，请告诉我你的.minecraft文件夹地址"
            )
            if not result: return 
            minecraft_path = folder_dialog("选择.minecraft文件夹")
            # 检查用户是否选择了文件夹（可能点击了取消）
            if not minecraft_path: return

            # 检查用户是否确认并提供有效的.minecraft/saves文件夹
            if result and os.path.exists(os.path.join(minecraft_path, 'saves')):
                # 保存minecraft路径到配置文件
                data['minecraft_path'] = minecraft_path
                write_data(data)
            else:
                # 用户取消或提供的路径无效，直接返回
                messagebox.showerror("错误", "不是有效的.minecraft文件夹")
                return

            messagebox.showinfo("提示", "成功! 现在来导入地图")
            # ====== 第三步：选择ZIP文件夹 ======
            zip_folder_path = folder_dialog("选择存放地图ZIP的文件夹")
            # 检查用户是否取消了第二次文件夹选择
            if not zip_folder_path: return # 用户取消了

        # ====== 第四步：获取ZIP文件列表 ======
        # 获取所有ZIP文件
        zip_files = glob.glob(os.path.join(zip_folder_path, '*.zip'))
        # 检查是否在选择的文件夹中找到任何ZIP文件
        if not zip_files:
            messagebox.showwarning("提示", "选择的文件夹中没有找到ZIP文件")
            return

        # ====== 第五步：创建进度窗口 ======
        progress_win, progress_bar, progress_label, file_label = self.progress_window("导入存档")
        total = len(zip_files)

        # ====== 第六步：解压ZIP文件 ======
        for i, zip_file in enumerate(zip_files, 1):
            # 获取ZIP文件名（不含扩展名）
            name = os.path.splitext(os.path.basename(zip_file))[0]
            
            # 更新进度显示
            file_label.configure(text=f"正在处理世界: {name}")
            progress_bar.set(i / total)
            progress_label.configure(text=f"{int(i / total * 100)}% ({i}/{total})")
            progress_win.update()

            # 执行解压操作
            zip_extract(
                zip_path=zip_file,
                extract_path=os.path.join(minecraft_path, 'saves'),
                name=name
            )

        # ====== 第七步：完成导入 ======
        # 完成后关闭进度条窗口
        progress_win.destroy()
        messagebox.showinfo("完成", f"成功导入 {total} 个存档")

    def export_save(self):
        """导出存档功能（待实现）

        Returns:
            None
        """
        messagebox.showinfo("功能开发中", "导出存档功能正在开发中，敬请期待！")

    def list_saves(self):
        """存档列表功能（待实现）

        Returns:
            None
        """
        messagebox.showinfo("功能开发中", "存档列表功能正在开发中，敬请期待！")

    def donate(self):
        """赞助功能，显示捐赠窗口，提供微信和支付宝支付选项

        Returns:
            None
        """
        donate_win = ctk.CTkToplevel(self.window)
        donate_win.title("感谢支持")
        donate_win.geometry("250x230")
        donate_win.transient(self.window)   # 置顶于主窗口
        donate_win.resizable(False, False)
        donate_win.tk.call('tk::PlaceWindow', donate_win.winfo_pathname(donate_win.winfo_id()), 'center')
        
        header_frame = ctk.CTkFrame(
            donate_win,
            fg_color="transparent"
        )
        header_frame.pack()
        
        # 标题
        title = ctk.CTkLabel(
            header_frame,
            text="请我喝杯水",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333"
        )
        title.pack(side="left", pady=(15, 5), padx=(0, 5))
        
        # 杯子图标
        cup_image = get_image("cup", (26, 26))
        cup = ctk.CTkLabel(
            master=header_frame, 
            image=cup_image, 
            text=""
        )
        cup.pack(side="left", pady=(8, 0))
        
        # 描述文字
        descripbe = ctk.CTkLabel(
            donate_win,
            text="如果你觉得这个工具帮到了你\n欢迎请我喝杯水（≤5元就行）\n你的支持是我更新的动力!",
            font=self.font_label,
            text_color="#383838",
            justify="center"
        )
        descripbe.pack(side="top", pady=(10, 0))
        
        # 按钮的配置
        btn_config = {
            "width": 90,
            "height": 40,
            "font": self.font_button,
            "anchor": "center",      # 整体居中
            "border_width": 2,
            "border_color": "#CFCFCF",
            "corner_radius": 13,
        }
        
        # 按钮容器
        buttons_row = ctk.CTkFrame(
            donate_win,
            fg_color="transparent",
            height=90,
        )
        buttons_row.pack(pady=(12, 5))
        
        # 微信按钮
        wechat_button = ctk.CTkButton(
            buttons_row, 
            text="微信",
            fg_color="#07C160",
            hover_color="#06AD56",
            text_color="#FFFFFF",
            command=lambda: self.show_donate_qr('wechat', donate_win),
            **btn_config,
        )
        wechat_button.pack(side="left", padx=(0, 10))
        
        # 支付宝按钮
        alipay_button = ctk.CTkButton(
            buttons_row,
            text="支付宝",
            fg_color="#1677FF",
            hover_color="#0D5FCC",
            text_color="#FFFFFF",
            command=lambda: self.show_donate_qr("alipay", donate_win),
            **btn_config
        )
        alipay_button.pack(side="left")
        
        # 分割线
        separator = ctk.CTkFrame(donate_win, height=2, fg_color="#E0E0E0")
        separator.pack(fill="x", padx=20, pady=5)
        
        # 协议文本
        licence_text = ctk.CTkLabel(
            donate_win,
            text="图标来源：Tabler Icons (MIT)",
            font=self.font_label,
            text_color="#888888"
        )
        licence_text.pack(side="bottom", pady=(0, 5))

    def show_donate_qr(self, platform:str, parent_win:ctk.CTkToplevel):
        """展示赞助码二维码窗口

        Args:
            platform (str): 支付平台类型，可选值为 'wechat'（微信）或 'alipay'（支付宝）
            parent_win (ctk.CTkToplevel): 父窗口对象，用于设置模态窗口关系

        Returns:
            None
        """
        qr_win = ctk.CTkToplevel(parent_win)
        qr_win.geometry("250x250")
        qr_win.transient(parent_win)    # 置顶于父窗口
        qr_win.tk.call('tk::PlaceWindow', qr_win.winfo_pathname(qr_win.winfo_id()), 'center')
        
        if platform == "wechat":
            qr_win.title("微信赞赏码")
        elif platform == "alipay":
            qr_win.title("支付宝赞赏码")
        
        qr_image = get_image(f"{platform}_qr", (220, 220))
        qr_label = ctk.CTkLabel(
            master=qr_win,
            image=qr_image, 
            text=""
        )
    
        qr_label.pack(expand=True)
        # 延迟设置模态，避免 grab failed
        qr_win.after(100, qr_win.grab_set)
            
    
    def progress_window(self, text: str):
        """创建进度条窗口

        Args:
            text (str): 进度条标题文本

        Returns:
            tuple: (progress_win, progress_bar, progress_label, file_label)
        """
        # 进度条窗口
        progress_win = ctk.CTkToplevel(self.window)
        progress_win.title("导入进度")
        progress_win.geometry("400x200")
        progress_win.transient(self.window)  # 置顶于主窗口
        progress_win.grab_set()  # 模态窗口
        progress_win.tk.call('tk::PlaceWindow', progress_win.winfo_pathname(progress_win.winfo_id()), 'center')

        

        ctk.CTkLabel(
            progress_win,
            text=f"正在{text}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        # 进度条
        progress_bar = ctk.CTkProgressBar(progress_win, width=300)
        progress_bar.pack(pady=10)
        progress_bar.set(0)  # 初始0%
        progress_win.update()

        # 进度文字
        progress_label = ctk.CTkLabel(
            progress_win,
            text="0% (0/0)",
            font=ctk.CTkFont(size=14)
        )
        progress_label.pack(pady=5)

        file_label = ctk.CTkLabel(
            progress_win,
            text="准备就绪",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        file_label.pack(pady=5)

        return progress_win, progress_bar, progress_label, file_label