from config import *
from utils import *


class App:
    def __init__(self):
        """GUI类"""
        self.window = ctk.CTk()
        self.window.title("🗃存档管理器")
        self.window.geometry("400x290")
        self.window.resizable(False, False)
        # self.window.iconbitmap(os.path.join(PROJECT_ROOT, "icon.ico"))  # 设置窗口图标（Linux不支持.ico格式）

        ctk.set_appearance_mode("light")

        self.create_header()  # 标题部分
        self.create_buttons()  # 按钮部分

    def create_header(self):
        header_frame = ctk.CTkFrame(self.window, fg_color="transparent")  # 存储容器
        header_frame.pack(pady=20)

        steve_image = get_image("steve", size=(32, 32))
        image_label = ctk.CTkLabel(header_frame, image=steve_image, text="")
        image_label.pack(side="left", padx=(0, 5))

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
            width=130,  # 固定宽度
            height=85,  # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.import_save,
            fg_color="#2c4068",
            hover_color="#1d2f53",
            text_color="#cfdaf2",
            image=get_image("map", (26, 26)),
            compound="bottom",
            anchor="center",
            border_width=2,
            corner_radius=13,
            border_color="#CFCFCF",
        )
        btn1.pack(side="left", padx=12)

        btn2 = ctk.CTkButton(
            row1,
            text="导出存档",
            width=130,  # 固定宽度
            height=85,  # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#793231",
            hover_color="#682d2c",
            text_color="#FBE3E3",
            image=get_image("box", (30, 30)),
            compound="bottom",
            anchor="center",
            border_width=2,
            border_color="#CFCFCF",
            corner_radius=13,
        )
        btn2.pack(side="left", padx=12)

        # 第二行容器(flex row)
        row2 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row2.pack(fill="both", pady=(20, 0))

        # 第二行两个按钮
        btn3 = ctk.CTkButton(
            row2,
            text="存档列表",
            width=130,  # 固定宽度
            height=85,  # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#795431",
            hover_color="#614021",
            text_color="#FFECDB",
            image=get_image("book_pen", (30, 30)),
            compound="bottom",
            anchor="center",
            border_width=2,
            border_color="#CFCFCF",
            corner_radius=13,
        )
        btn3.pack(side="left", padx=12)

        btn4 = ctk.CTkButton(
            row2,
            text="赞助一下",
            width=130,  # 固定宽度
            height=85,  # 固定高度
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#6E9D28",
            hover_color="#5C861C",
            text_color="#F7FFEC",
            image=get_image("golden_apple", (30, 30)),
            compound="bottom",
            anchor="center",
            border_width=2,
            border_color="#CFCFCF",
            corner_radius=13,
        )
        btn4.pack(side="left", padx=12)

    def import_save(self):
        # GUI: 导入存档
        print("import_save 方法被调用")  # 调试日志
        data = read_data()
        print(f"读取的数据: {data}")  # 调试日志

        minecraft_path = data.get("minecraft_path", "")
        print(f"minecraft_path: {minecraft_path}")  # 调试日志

        # 检查并获取 minecraft 文件夹路径
        if not minecraft_path:  # 如果没有记录的路径
            result = messagebox.askyesno(
                "温馨提示", "导入存档前，请先配置你的.minecraft文件夹地址。\n是否现在配置？"
            )

            if not result:
                messagebox.showwarning("取消", "已取消导入存档")
                return

            minecraft_path = foder_dialog("选择.minecraft文件夹")
            if not minecraft_path:
                messagebox.showwarning("取消", "未选择.minecraft文件夹，已取消导入")
                return

            # 检查 saves 文件夹
            saves_path = os.path.join(minecraft_path, "saves")
            if os.path.exists(saves_path):
                # 保存配置
                data["minecraft_path"] = minecraft_path
                write_data(data)
                messagebox.showinfo(
                    "配置成功", "minecraft文件夹配置成功！\n现在选择存放地图ZIP的文件夹"
                )
            else:
                messagebox.showerror(
                    "错误",
                    f"未在选择的文件夹中找到 'saves' 文件夹。\n"
                    f"请确认选择的是正确的.minecraft文件夹。\n"
                    f"选择的路径：{minecraft_path}",
                )
                return

            zip_folder_path = foder_dialog("选择存放地图ZIP的文件夹")
        else:
            # 检查已保存的路径是否有效
            if not os.path.exists(minecraft_path):
                messagebox.showwarning(
                    "路径无效", "之前配置的.minecraft文件夹路径已不存在。\n请重新配置"
                )
                minecraft_path = foder_dialog("选择.minecraft文件夹")
                if not minecraft_path:
                    messagebox.showwarning("取消", "未选择.minecraft文件夹，已取消导入")
                    return

                saves_path = os.path.join(minecraft_path, "saves")
                if not os.path.exists(saves_path):
                    messagebox.showerror(
                        "错误", f"未找到 'saves' 文件夹。\n请确认选择的是正确的.minecraft文件夹"
                    )
                    return

                data["minecraft_path"] = minecraft_path
                write_data(data)

            zip_folder_path = foder_dialog("选择存放地图ZIP的文件夹")

        # 检查是否选择了文件夹
        if not zip_folder_path:
            messagebox.showwarning("取消", "未选择文件夹，已取消导入")
            return

        # 获取所有zip文件
        zip_files = glob.glob(os.path.join(zip_folder_path, "*zip"))

        # 检查是否有zip文件
        if not zip_files:
            messagebox.showwarning(
                "未找到文件",
                f"在选择的文件夹中未找到任何ZIP文件。\n请确保选择的是包含地图ZIP文件的文件夹。\n路径：{zip_folder_path}",
            )
            return

        # 显示进度条并开始导入
        progress_win, progress_bar, progress_label, file_label = self.progress_window("导入存档")

        total = len(zip_files)
        success_count = 0
        error_count = 0

        for i, zip_file in enumerate(zip_files, 1):
            zip_path = os.path.join(zip_file)
            name = os.path.splitext(os.path.basename(zip_file))[0]

            # 更新进度条
            file_label.configure(text=f"正在处理世界: {name}")
            progress_bar.set(i / total)
            progress_label.configure(text=f"{int(i / total * 100)}% ({i})/({total})")
            progress_win.update()

            try:
                # 执行解压操作
                zip_extract(
                    zip_path=zip_path, extract_path=os.path.join(minecraft_path, "saves"), name=name
                )
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"解压失败: {name}, 错误: {e}")

        progress_win.destroy()

        # 显示结果
        if error_count == 0:
            messagebox.showinfo("完成", f"成功导入 {success_count} 个存档")
        else:
            messagebox.showwarning(
                "完成（有错误）",
                f"成功导入 {success_count} 个存档\n失败 {error_count} 个存档\n请检查控制台查看详细错误信息",
            )

    def progress_window(self, text: str):
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
        progress_win.transient(self.window)  # 置顶于主窗口
        progress_win.grab_set()  # 模态窗口

        ctk.CTkLabel(
            progress_win, text=f"正在{text}", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        # 进度条
        progress_bar = ctk.CTkProgressBar(progress_win, width=300)
        progress_bar.pack(pady=10)
        progress_bar.set(0)  # 初始0%
        progress_win.update()

        # 进度文字
        progress_label = ctk.CTkLabel(progress_win, text="0% (0/0)", font=ctk.CTkFont(size=14))
        progress_label.pack(pady=5)

        file_label = ctk.CTkLabel(
            progress_win, text="准备就绪", font=ctk.CTkFont(size=12), text_color="gray"
        )
        file_label.pack(pady=5)

        return progress_win, progress_bar, progress_label, file_label
