from config import *
from utils import get_image

class App:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🗃存档管理器")
        self.window.geometry("400x290")

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
            text_color="#546EA0",  # 主题蓝色
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
        # 创建新窗口
        import_window = ctk.CTkToplevel(self.window)
        import_window.title("导入存档")
        import_window.geometry("500x400")

app = App()
app.window.mainloop()