from config import *
from utils import *
from message import Message


class App:
    # ==================== 初始化方法 ====================
    def __init__(self):
        """GUI应用程序类初始化
        
        逻辑流程:
            创建主窗口
            ↓
            设置窗口属性 (尺寸、标题、颜色)
            ↓
            加载字体文件
            ↓
            创建 UI (标题 + 按钮)
            ↓
            窗口居中
            ↓
            播放启动音效

        Returns:
            None
        """
        
        self.window: ctk.CTk = ctk.CTk()
        self.window.geometry("550x290")
        self.window.title("Minecraft 存档管理器")
        self.window.resizable(False, False)
        self.window.configure(fg_color="#E0E5EC")
        
        ctk.set_appearance_mode("light")

        # 加载字体文件
        ctk.FontManager.load_font(str(path_config.FONT_REGULAR_PATH))
        ctk.FontManager.load_font(str(path_config.FONT_MEDIUM_PATH))

        # 设置组件字体
        self.font_text: callable = lambda size, weight="normal": ctk.CTkFont(family=path_config.FONT_REGULAR_NAME, size=size, weight=weight)  # type:ignore

        self.create_header()    # 标题部分
        self.create_buttons()   # 按钮部分

        playsound(path_config.get_sound_path("start.mp3"), block=False)
        # 窗口居中
        center_window(self.window)

    # ==================== UI 创建方法 ====================
    def create_header(self):
        """创建标题区域，显示应用名称和图标

        逻辑流程:
            创建透明容器
            ↓
            加载并显示图标
            ↓
            显示应用标题 "存档管理器"

        Returns:
            None
        """
        header_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        header_frame.pack(pady=20)

        steve_image = get_image("icon", size=(32, 32))
        image_label = ctk.CTkLabel(header_frame, image=steve_image, text="")
        image_label.pack(side="left", padx=(0, 10))

        # 大标题
        title = ctk.CTkLabel(
            header_frame,
            text="存档管理器",
            font=self.font_text(24),
            text_color="#333333",
        )
        title.pack(side="left")

    def create_buttons(self):
        """创建功能按钮区域，包含导入存档、导出存档、存档列表、赞助一下四个按钮

        逻辑流程:
            创建按钮容器
            ├─ 第一行按钮
            │   ├─ 导入存档
            │   ├─ 导出存档 (待实现)
            │   └─ 存档列表 (待实现)
            └─ 第二行按钮
                ├─ 存档修复 (待实现)
                ├─ 赞助一下
                └─ 关于软件 (待实现)

        Returns:
            None
        """
        # 按钮容器
        btn_container = ctk.CTkFrame(self.window, fg_color="transparent")
        btn_container.pack(padx=45)

        # 第一行容器
        row1 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row1.pack(fill="both", pady=(0, 15))

        # 第二行容器
        row2 = ctk.CTkFrame(btn_container, fg_color="transparent")
        row2.pack(fill="both")

        # 按钮默认参数
        btn_config = {
            "width": 130,
            "height": 85,
            "font": self.font_text(16),
            "compound": "bottom",  # 文字在底部，图片在顶部
            "anchor": "center",  # 整体居中
            "border_width": 4,
            "border_color": "#B3B3B3",
            "corner_radius": 13,
        }

        # 第一行按钮：导入存档
        import_save = ctk.CTkButton(
            row1,
            text="导入存档",
            command=self.import_save,
            fg_color="#2c4068",
            hover_color="#1d2f53",
            text_color="#cfdaf2",
            image=get_image("import", (26, 26)),
            **btn_config,
        )
        import_save.pack(side="left", padx=12)

        # 第一行按钮：导出存档
        export_save = ctk.CTkButton(
            row1,
            text="导出存档",
            command=self.export_save,
            fg_color="#793231",
            hover_color="#682d2c",
            text_color="#FBE3E3",
            image=get_image("export", (30, 30)),
            **btn_config,
        )
        export_save.pack(side="left", padx=12)

        # 第一行按钮：存档列表
        list_save = ctk.CTkButton(
            row1,
            text="存档列表",
            command=self.list_saves,
            fg_color="#795431",
            hover_color="#614021",
            text_color="#FFECDB",
            image=get_image("list", (30, 30)),
            **btn_config,
        )
        list_save.pack(side="left", padx=12)

        # 第二行按钮：存档修复
        fix_save = ctk.CTkButton(
            row2,
            text="存档修复",
            # command=,
            fg_color="#D2932E",
            hover_color="#C48828",
            text_color="#FFF8EC",
            image=get_image("tool", (30, 30)),
            **btn_config,
        )
        fix_save.pack(side="left", padx=12)

        # 第二行按钮：赞助一下
        donate = ctk.CTkButton(
            row2,
            text="赞助一下",
            command=self.donate,
            fg_color="#6E9D28",
            hover_color="#638F22",
            text_color="#F7FFEC",
            image=get_image("donate", (30, 30)),
            **btn_config,
        )
        donate.pack(side="left", padx=12)

        # 第二行按钮：关于
        about = ctk.CTkButton(
            row2,
            text="关于软件",
            command=self.about,
            fg_color="#28519D",
            hover_color="#1F468F",
            text_color="#E3EDFF",
            image=get_image("about", (30, 30)),
            **btn_config,
        )
        about.pack(side="left", padx=12)

    # ==================== 核心功能方法 ====================
    def import_save(self) -> None:
        """导入存档功能，将ZIP格式的地图文件解压到Minecraft的saves文件夹
        
        逻辑流程:
            读取用户配置 (data.json)
            ↓
            获取 Minecraft saves 路径 → _get_saves_path()
            ↓ (失败返回)
            选择 ZIP 文件夹
            ↓ (取消返回)
            获取 ZIP 文件列表
            ↓ (无文件提示错误)
            批量解压 ZIP → _extract_zip_files()

        Returns:
            None
        """
        # 获取数据文件
        data: dict = read_data()  # 获取数据文件
        
        # 获取.minecraft路径
        saves_path: str | None = self._get_saves_path(data=data)
        if saves_path is None:  # 获取到了saves文件夹了路径
            return
        
        # 选择ZIP文件夹
        zip_folder_path: str = folder_dialog("选择存放地图ZIP的文件夹")
        # 检查用户是否取消了第二次文件夹选择
        if not zip_folder_path: return # 用户取消了

        # 获取ZIP文件列表
        zip_files: list[Path] = list(Path(zip_folder_path).glob("*.zip"))
        # 检查是否在选择的文件夹中找到任何ZIP文件
        if not zip_files:
            Message(self.window).info(
                "错误",
                "选择的文件夹中没有找到ZIP文件",
                self.font_text(14)
            )
            return

        # 进行逐个解压
        self._extract_zip_files(zip_files=zip_files, saves_path=saves_path)

    def export_save(self) -> None:
        """导出存档功能（待实现）

        Returns:
            None
        """
        Message(self.window).info(
            "功能开发中", "导出存档功能正在开发中，敬请期待！", self.font_text(14)
        )

    def list_saves(self) -> None:
        """存档列表功能，显示所有存档的列表

        逻辑流程:
            获取存档列表信息 → get_saves_data()
            ↓ (无存档返回)
            检查是否有存档
            ↓
            创建存档列表窗口
            ↓
            创建可滚动框架
            ↓
            遍历所有版本和存档
            ├─ 创建卡片框架
            ├─ 添加存档名称标签
            └─ 添加版本号标签
            ↓
            显示存档列表窗口

        Returns:
            None
        """
        # 获取存档列表信息
        saves_data: dict | list | None = get_saves_data()
        if saves_data is None:
            ask: bool = Message(self.window).yes_no(
                "错误", "未检测到任何存档，是否选择告诉我你的.minecraft文件夹?", self.font_text(14)
            )
            if ask:
                data: dict | None = self._set_minecraftPath(data=read_data())
                if data:  # 如果用户选择正确
                    write_data(data)
                    saves_data = get_saves_data()
                    if saves_data is None:
                        return
                else:
                    return
            else:  # 用户不想操作
                return

        # 创建存档列表窗口
        saves_win = ctk.CTkToplevel(self.window)
        saves_win.title("存档列表")
        saves_win.geometry("400x300")
        saves_win.transient(self.window)  # 置顶于主窗口
        saves_win.resizable(False, False)
        saves_win.after(100, lambda: saves_win.grab_set())

        center_window(saves_win)  # 窗口居中

        # 创建可滚动框架
        scroll_frame = ctk.CTkScrollableFrame(
            saves_win,
            width=400,
            height=300,
            fg_color="transparent",
        )
        scroll_frame.pack(side="top", fill="both")

        for i in saves_data:
            for j in saves_data[i]:
                # 单个卡片框架
                card = ctk.CTkFrame(
                    scroll_frame,
                    width=350,
                    height=50,
                    fg_color="transparent",
                    border_color="#DDDDDD",
                    border_width=2,
                    corner_radius=5,
                )
                card.pack(side="top", pady=(10, 0), padx=5, fill="x")

                # 文本框架
                text_frame = ctk.CTkFrame(
                    card,
                    fg_color="transparent",
                )
                text_frame.pack(side="left", pady=(5, 5), padx=(5, 0))

                # 存档名称
                save_name = ctk.CTkLabel(
                    text_frame,
                    text=f"{limit_name_length(j, 30)}",
                    font=self.font_text(14, "bold"),
                    text_color="#63835D",
                )
                save_name.pack(side="top", anchor="w", padx=(15, 0))

                # 版本号
                version_name = ctk.CTkLabel(
                    text_frame,
                    text=f"{i}",
                    font=self.font_text(13, "bold"),
                    text_color="#434343",
                )
                version_name.pack(side="top", anchor="w", padx=(15, 0))

        saves_win.update()  # 更新窗口

    def donate(self) -> None:
        """赞助功能，显示捐赠窗口，提供微信和支付宝支付选项

        逻辑流程:
            创建赞助窗口
            ↓
            显示标题和杯子图标
            ↓
            显示描述文字
            ↓
            显示微信/支付宝按钮
            ↓
            点击按钮 → 显示二维码 → _show_donate_qr()

        Returns:
            None
        """
        donate_win = ctk.CTkToplevel(self.window)
        donate_win.title("感谢支持")
        donate_win.geometry("340x250")
        donate_win.transient(self.window)  # 置顶于主窗口
        donate_win.resizable(False, False)
        center_window(donate_win)  # 窗口居中

        header_frame = ctk.CTkFrame(donate_win, fg_color="transparent")
        header_frame.pack()

        # 标题
        title = ctk.CTkLabel(
            header_frame,
            text="请我喝杯水",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#333333",
        )
        title.pack(side="left", pady=(15, 5), padx=(0, 5))

        # 杯子图标
        cup_image = get_image("cup", (26, 26))
        cup = ctk.CTkLabel(master=header_frame, image=cup_image, text="")
        cup.pack(side="left", pady=(8, 0))

        # 描述文字
        describe = ctk.CTkLabel(
            donate_win,
            text="如果你觉得这个工具帮到了你\n欢迎请我喝杯水（≤5元就行）\n你的支持是我更新的动力!",
            font=self.font_text(14),
            text_color="#383838",
            justify="center",
        )
        describe.pack(side="top", pady=(10, 0))

        # 按钮的配置
        btn_config = {
            "width": 90,
            "height": 40,
            "font": self.font_text(16),
            "anchor": "center",  # 整体居中
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
            command=lambda: self._show_donate_qr("wechat", donate_win),
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
            command=lambda: self._show_donate_qr("alipay", donate_win),
            **btn_config,
        )
        alipay_button.pack(side="left")

        # 分割线
        separator = ctk.CTkFrame(donate_win, height=2, fg_color="#E0E0E0")
        separator.pack(fill="x", padx=20, pady=5)

        # 协议文本
        licence_text = "图标：Tabler Icons (MIT)\n音效：Pixabay.com\n字体：HarmonyOS Sans (免费商用)"

        licence = ctk.CTkLabel(
            donate_win,
            text=licence_text,
            font=self.font_text(14),
            text_color="#888888",
        )
        licence.pack(pady=(0, 5))

    def about(self) -> None:
        """关于软件功能，显示软件信息（待实现）

        逻辑流程:
            显示提示信息
            ↓
            告知用户功能正在开发中

        Returns:
            None
        """
        Message(self.window).info(
            "功能开发中", "关于软件功能正在开发中，敬请期待！", self.font_text(14)
        )

    # ==================== 辅助功能方法 ====================
    def _get_saves_path(self, data: dict) -> str | None:
        """获取 Minecraft saves 文件夹路径

        逻辑流程:
            检查是否已有配置
            ├─ 分支 1: 已有路径 + 非版本迁移
            │   └─ 返回 minecraft_path/saves
            ├─ 分支 2: 已有路径 + 版本迁移
            │   ├─ 选择游戏版本 → _select_version_saves()
            │   └─ 返回 minecraft_path/versions/{版本}/saves
            └─ 分支 3: 无配置
                ├─ 询问用户
                ├─ 选择 .minecraft 文件夹
                ├─ 验证文件夹有效性
                ├─ 保存配置到 data.json
                └─ 返回相应的 saves 路径

        Args:
            data: 用户配置字典

        Returns:
            str|None: saves文件夹路径，失败返回None
        """
        minecraft_path: str = data["minecraft_path"]
        migrate: bool = data["migrate"]
        saves_path: str = ""

        # 检查用户是否已经保存过.minecraft文件夹路径
        if (
            minecraft_path and not migrate
        ):  # 用户已记录一个没有版本迁移minecraft文件夹路径
            saves_path = str(Path(minecraft_path, "saves"))
            return saves_path
        elif minecraft_path and migrate:  # 用户已记录一个版本迁移的
            # 选择版本
            select_version = self._select_version_saves(minecraft_path)
            if not select_version:
                return None
            else:
                saves_path = str(
                    Path(minecraft_path, "versions", select_version, "saves")
                )
                return saves_path
        else:  # 如果没有记录
            # 询问用户是否愿意提供.minecraft文件夹路径
            ask = Message(self.window).yes_no(
                "温馨提示",
                "导入存档前，请告诉我你的.minecraft文件夹地址",
                self.font_text(14),
            )
            if not ask:
                return None

            minecraft_path: str = folder_dialog("选择.minecraft文件夹")

            # 检查用户是否选择了文件夹（可能点击了取消）
            if not minecraft_path:
                return None

            check: dict = is_minecraft_folder(minecraft_path)

            # 检查用户是否确认并提供有效的.minecraft/saves文件夹
            if check["find"] and check["migrate"]:  # 如果是版本迁移
                data["minecraft_path"] = minecraft_path
                data["migrate"] = True

                # 让用户选择迁移版本
                select_version = self._select_version_saves(minecraft_path)
                if not select_version:  # 用户没有选择版本
                    # 保存文件
                    write_data(data)
                    return None
                else:
                    saves_path = str(
                        Path(minecraft_path, "versions", select_version, "saves")
                    )
                    # 保存文件
                    write_data(data)
                    Message(self.window).info(
                        "提示", "成功! 现在来导入地图", self.font_text(14)
                    )
                    return saves_path

            elif check["find"] and not check["migrate"]:  # 不是版本迁移
                data["minecraft_path"] = minecraft_path
                saves_path = str(Path(minecraft_path, "saves"))

                Message(self.window).info(
                    "提示", "成功! 现在来导入地图", self.font_text(14)
                )

                # 保存文件
                write_data(data)
                return saves_path
            elif not check["find"]:
                # 用户取消或提供的路径无效，直接返回
                Message(self.window).info(
                    "错误", "不是有效的.minecraft文件夹", self.font_text(14)
                )
                return None

    def _select_version_saves(self, minecraft_path: str) -> str:
        """让用户选择要迁移到哪个版本

        逻辑流程:
            检查 versions 文件夹是否存在
            ↓
            获取版本列表
            ↓
            创建版本选择窗口
            ↓
            显示单选按钮列表
            ↓
            用户确认 → 返回选中的版本

        Args:
            minecraft_path: .minecraft 文件夹路径

        Returns:
            str: 选择的版本名称，取消则返回空字符串
        """
        btn_config = {
            "width": 90,
            "height": 40,
            "anchor": "center",  # 整体居中
            "border_width": 2,
            "border_color": "#CFCFCF",
            "corner_radius": 13,
        }

        # 获取版本列表
        if not Path(minecraft_path, "versions").exists():
            return ""

        versions_folders = Path(minecraft_path, "versions").iterdir()
        versions_names = [p.name for p in versions_folders]
        if not versions_names:
            return ""

        # 创建窗口
        win = ctk.CTkToplevel(
            self.window,
        )
        win.title("选择你的游戏版本")

        # 动态计算窗口大小
        item_height = 35  # 每个选项占的高度
        button_height = 60  # 确定按钮占的高度
        max_height = 500  # 最大高度

        win_height = min(len(versions_names) * item_height + button_height, max_height)

        win.geometry(f"400x{win_height}")

        # 模态化和置顶主窗口
        win.after(100, win.grab_set)  # 延迟设置模
        win.transient(self.window)

        # 居中窗口
        center_window(win)

        # 遍历列表
        selected_version = ctk.StringVar(value="")  # 绑定选择结果

        for name in versions_names:
            frame = ctk.CTkFrame(master=win, fg_color="transparent")
            frame.pack(pady=(3, 3))

            # 文字标签
            label = ctk.CTkLabel(
                frame,
                text=name,
                font=self.font_text(14),
            )
            label.pack(side="left")

            # 单选按钮
            radio = ctk.CTkRadioButton(
                frame,
                variable=selected_version,
                value=name,
                width=20,
                text="",
            )
            radio.pack(side="left", padx=(10, 0))

        # 设置初始值为空，避免因为选择了后关闭窗口，还会返回有效值
        result = ""

        def on_confirm():
            nonlocal result
            result = selected_version.get()
            win.destroy()

        buttons_frame = ctk.CTkFrame(win, fg_color="transparent")

        buttons_frame.pack(pady=(5, 0))

        yes_button = ctk.CTkButton(
            buttons_frame,
            text="确认",
            fg_color="#86aa19",
            hover_color="#799b16",
            command=on_confirm,
            **btn_config,
        )
        no_button = ctk.CTkButton(
            buttons_frame, text="取消", command=win.destroy, **btn_config
        )

        yes_button.pack(side="left", padx=(0, 15))
        no_button.pack(side="left")

        win.wait_window()

        return result

    def _show_donate_qr(self, platform: str, parent_win: ctk.CTkToplevel) -> None:
        """展示赞助码二维码窗口

        逻辑流程:
            创建二维码窗口
            ↓
            根据平台设置标题
            ↓
            加载并显示二维码图片
            ↓
            设置为模态窗口

        Args:
            platform (str): 支付平台类型，可选值为 "wechat"（微信）或 "alipay"（支付宝）
            parent_win (ctk.CTkToplevel): 父窗口对象，用于设置模态窗口关系

        Returns:
            None
        """
        qr_win = ctk.CTkToplevel(parent_win)
        qr_win.geometry("250x250")
        qr_win.transient(parent_win)  # 置顶于父窗口
        center_window(qr_win)  # 窗口居中

        if platform == "wechat":
            qr_win.title("微信赞赏码")
        elif platform == "alipay":
            qr_win.title("支付宝赞赏码")

        qr_image = get_image(f"{platform}_qr", (220, 220))
        qr_label = ctk.CTkLabel(master=qr_win, image=qr_image, text="")

        qr_label.pack(expand=True)
        # 延迟设置模态，避免 grab failed
        qr_win.after(100, qr_win.grab_set)

    def _progress_window(self, text: str) -> tuple[ctk.CTkToplevel, ctk.CTkProgressBar, ctk.CTkLabel, ctk.CTkLabel]:
        """创建进度条窗口

        逻辑流程:
            创建进度窗口
            ↓
            显示标题
            ↓
            创建进度条组件
            ↓
            创建进度文字标签
            ↓
            创建文件名标签
            ↓
            返回所有组件引用

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
        center_window(progress_win)  # 窗口居中

        ctk.CTkLabel(
            progress_win, text=f"正在{text}", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        # 进度条
        progress_bar = ctk.CTkProgressBar(progress_win, width=300)
        progress_bar.pack(pady=10)
        progress_bar.set(0)  # 初始0%
        progress_win.update()

        # 进度文字
        progress_label = ctk.CTkLabel(
            progress_win, text="0% (0/0)", font=ctk.CTkFont(size=14)
        )
        progress_label.pack(pady=5)

        file_label = ctk.CTkLabel(
            progress_win, text="准备就绪", font=ctk.CTkFont(size=12), text_color="gray"
        )
        file_label.pack(pady=5)

        return progress_win, progress_bar, progress_label, file_label

    def _extract_zip_files(self, zip_files: list[Path], saves_path: str) -> None:
        """批量解压ZIP文件到指定目录

        逻辑流程:
            创建进度窗口
            ↓
            遍历所有 ZIP 文件
            ├─ 检查存档是否已存在
            │   └─ 询问是否覆盖
            ├─ 更新进度显示
            └─ 执行解压 → zip_extract()
            ↓
            关闭进度窗口
            ↓
            显示完成提示

        Args:
            zip_files: ZIP文件列表
            saves_path: 目标saves文件夹路径

        Returns:
            None
        """
        # 创建进度窗口
        progress_win, progress_bar, progress_label, file_label = self._progress_window(
            "导入存档"
        )
        total = len(zip_files)  # 任务量

        # 解压ZIP文件
        success_count = 0
        for i, zip_file in enumerate(zip_files, 1):
            # 获取ZIP文件名（不含扩展名）
            name = Path(zip_file).stem
            target = Path(saves_path) / name

            if target.exists():
                result = Message(self.window).yes_no(
                    "存档已存在", f"{name} 存档已存在，是否覆盖", self.font_text(14)
                )
                if not result:  # 不要覆盖
                    continue  # 进行跳过
                else:  # 进行覆盖
                    shutil.rmtree(target)

            # 更新进度显示
            file_label.configure(text=f"正在处理世界: {name}")
            progress_bar.set(i / total)
            progress_label.configure(text=f"{int(i / total * 100)}% ({i}/{total})")
            progress_win.update()

            # 执行解压操作
            zip_extract(zip_path=str(zip_file), extract_path=str(saves_path), name=name)
            success_count += 1

        # 完成后关闭进度条窗口
        progress_win.destroy()
        Message(self.window).info(
            "完成", f"成功导入 {success_count} 个存档", self.font_text(14)
        )

    def _set_minecraftPath(self, data: dict) -> dict | None:
        """设置Minecraft路径
        
        逻辑流程:
            选择.minecraft文件夹
            ↓
            检查用户是否选择了文件夹
            ↓
            验证文件夹是否为有效的.minecraft文件夹
            ↓
            如果有效，更新配置数据
            ↓
            返回更新后的数据或None

        Args:
            data: 用户配置字典

        Returns:
            dict | None: 更新后的配置数据，如果选择失败或路径无效则返回None
        """
        minecraft_path: str = folder_dialog("选择.minecraft文件夹")
        # 检查用户是否选择了文件夹
        if not minecraft_path:
            return None

        check: dict = is_minecraft_folder(minecraft_path)

        if check["find"]:
            data["minecraft_path"] = minecraft_path
            data["migrate"] = check["migrate"]
            return data
        else:
            Message(self.window).info(
                "错误", "不是有效的.minecraft文件夹", self.font_text(14)
            )
            return None
