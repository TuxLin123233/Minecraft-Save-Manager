from config import *
from utils import *

class App:
    def __init__(self):
        """GUI类
        """
        self.window = ctk.CTk()
        self.window.title("🗃存档管理器")
        self.window.geometry("400x290")
        self.window.resizable(False, False)
        
        ctk.set_appearance_mode("light")
        
        self.create_header()    # 标题部分
        self.create_buttons()   # 按钮部分
        

    def create_header(self):
        header_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )     # 存储容器
        header_frame.pack(pady=20)

        steve_image = get_image('steve', size=(32, 32))
        image_label = ctk.CTkLabel(
            header_frame, 
            image=steve_image,
            text=""
        )
        image_label.pack(side='left', padx=(0, 5))

        # 大标题
        title = ctk.CTkLabel(
            header_frame,
            text="Minecraft 存档管理器",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#333333",  # 主题蓝色
        )
        title.pack(side="left")

    def create_buttons(self):
        # 按钮容器(整个区域)
        btn_container = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_container.pack(expand=True, fill="both", padx=45)

        # 第一行容器(flex row)
        row1 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row1.pack(fill="both")

        # 第一行两个按钮
        btn1 = ctk.CTkButton(
            row1,
            text="导入存档",
            width=130,           # 固定宽度
            height=85,           # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.import_save,
            fg_color="#2c4068",
            hover_color="#1d2f53",
            text_color="#cfdaf2",
            image=get_image('map', (26, 26)),
            compound="bottom",
            anchor="center",
            border_width=2,
            corner_radius=13,
            border_color="#CFCFCF"
        )
        btn1.pack(side="left", padx=12)

        btn2 = ctk.CTkButton(
            row1,
            text="导出存档",
            width=130,           # 固定宽度
            height=85,           # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.import_save,
            fg_color="#793231",
            hover_color="#682d2c",
            text_color="#FBE3E3",
            image=get_image('box', (30, 30)),
            compound="bottom",
            anchor="center",
            border_width=2,
            border_color="#CFCFCF",
            corner_radius=13
        )
        btn2.pack(side="left", padx=12)

        # 第二行容器(flex row)
        row2 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row2.pack(fill="both", pady=(20, 0))

        # 第二行两个按钮
        btn3 = ctk.CTkButton(
            row2,
            text="存档列表",
            width=130,           # 固定宽度
            height=85,           # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.import_save,
            fg_color="#795431",
            hover_color="#614021",
            text_color="#FFECDB",
            image=get_image('book_pen', (30, 30)),
            compound="bottom",
            anchor="center",
            border_width=2,
            border_color="#CFCFCF",
            corner_radius=13
        )
        btn3.pack(side="left", padx=12)

        btn4 = ctk.CTkButton(
            row2,
            text="赞助一下",
            width=130,           # 固定宽度
            height=85,           # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.import_save,
            fg_color="#6E9D28",
            hover_color="#5C861C",
            text_color="#F7FFEC",
            image=get_image('golden_apple', (30, 30)),
            compound="bottom",
            anchor="center",
            border_width=2,
            border_color="#CFCFCF",
            corner_radius=13
        )
        btn4.pack(side="left", padx=12)

    def import_save(self):
        # GUI: 导入存档
        data=read_data()
        
        minecraft_path = data['minecraft_path']
        if minecraft_path:  # 用户有记录minecraft文件夹路径
            zip_folder_path = foder_dialog("选择存放地图ZIP的文件夹")
            if not zip_folder_path:
                return 
        else:   # 如果没有
            result:bool = messagebox.askyesno(
                "温馨提示",
                "导入存档前，请告诉我你的.minecraft文件夹地址"
            )
            
            minecraft_path = foder_dialog("选择.minecraft文件夹")
            if not minecraft_path: return 
            
            if result and os.path.exists(os.path.join(minecraft_path, 'saves')):
                # 填充本地minecraft_path
                data['minecraft_path'] = minecraft_path
                write_data(data)
            else: return 
                    
        
            messagebox.showinfo("提示", "成功! 现在来导入地图")
            zip_folder_path = foder_dialog("选择存放地图ZIP的文件夹")
            if not zip_folder_path: return    # 用户取消了
        
        
        # 获取所有zip的迭代器
        zip_files = glob.glob(os.path.join(zip_folder_path, '*zip'))
        
        progress_win, progress_bar, progress_label, file_label = self.progress_window("导入存档")
        
        total = len(zip_files)  # 文件个数
        for i, zip_file in enumerate(zip_files, 1):
            # 获取每个zip文件的路径
            zip_path = os.path.join(zip_file)
            # 获取zip名
            name = os.path.splitext(os.path.basename(zip_file))[0]
            
            # 进度条更新参数
            file_label.configure(text=f"正在处理世界: {name}")
            progress_bar.set(i / total)
            progress_label.configure(text=f"{int(i / total * 100)}% ({i})/({total})")
            progress_win.update()
            
            # 执行解压操作
            zip_extract(
                zip_path=zip_path,
                extract_path=os.path.join(minecraft_path, 'saves'), 
                name=name
            )
        
        progress_win.destroy()
        messagebox.showinfo("完成", f"成功导入 {total} 个存档")
            
        
    def progress_window(self, text:str):
        """进度条窗口

        Args:
            text (str): 内容

        Returns:
            _type_: progress_win(窗口), progress_bar(进度条模块), progress_label(进度提示标签), file_label(文件提示标签)
        """
        # 进度条窗口
        progress_win = ctk.CTkToplevel(self.window)
        progress_win.title("导入进度")
        progress_win.geometry("400x200")
        progress_win.transient(self.window)     # 置顶于主窗口
        progress_win.grab_set()     # 模态窗口
        
        ctk.CTkLabel(
            progress_win, 
            text=f"正在{text}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # 进度条
        progress_bar = ctk.CTkProgressBar(
            progress_win,
            width=300
        )
        progress_bar.pack(pady=10)
        progress_bar.set(0)     # 初始0%
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