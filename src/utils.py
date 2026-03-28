from config import *


def zip_extract(zip_path: str, extract_path: str, name: str) -> None:
    """解压ZIP存档到指定目录
    
    逻辑流程:
        检查临时目录是否存在，不存在则创建
        ↓
        验证ZIP文件有效性
        ↓
        解压ZIP文件到临时目录
        ↓
        获取临时目录中的所有内容
        ↓
        验证ZIP文件有内容
        ↓
        获取解压的第一个项目
        ↓
        移动并重新命名到目标目录

    Args:
        zip_path: ZIP压缩包路径
        extract_path: 解压目标目录路径
        name: 存档名称（与ZIP文件名相同）

    Returns:
        None
        
    Raises:
        zipfile.BadZipFile: 如果文件不是有效的ZIP文件
        ValueError: 如果ZIP文件中没有可提取的内容
    """
    if not path_config.TEMP_PATH.exists():
        path_config.TEMP_PATH.mkdir(exist_ok=True)

    # 验证ZIP文件有效性
    if not zipfile.is_zipfile(zip_path):
        raise zipfile.BadZipFile(f"文件不是有效的ZIP文件: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(path_config.TEMP_PATH)

    extracted_items = list(Path(path_config.TEMP_PATH).glob("*"))
    if not extracted_items:
        raise ValueError(f"ZIP文件 {zip_path} 中没有找到可提取的内容")

    origin_path = extracted_items[0]
    shutil.move(origin_path, Path(extract_path) / name)


def get_image(image_name: str, size: tuple) -> ctk.CTkImage:
    """获取CTkImage图像对象（支持缩放）
    
    逻辑流程:
        检查是否在PyInstaller打包环境中运行
        ├─ 打包环境
        │   ├─ 获取临时解压目录 (sys._MEIPASS)
        │   └─ 构建图片路径 (sys._MEIPASS/img/{name}.png)
        └─ 开发环境
            ├─ 获取项目根目录
            └─ 构建图片路径 (项目根目录/img/{name}.png)
        ↓
        打开PIL图像
        ↓
        创建CTkImage对象并返回

    Args:
        image_name: img文件夹中的PNG文件名（不含扩展名）
        size: 图片尺寸元组 (width, height)

    Returns:
        ctk.CTkImage: 可缩放图像对象
    """
    import sys
    
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS    # type:ignore
        img_path = Path(base_path, "img", f"{image_name}.png")
    else:
        base_dir = Path(__file__).parent
        project_root = base_dir.parent
        img_path = project_root / "img" / f"{image_name}.png"
    
    pil_image = Image.open(img_path)
    
    return ctk.CTkImage(
        light_image=pil_image,
        dark_image=pil_image,
        size=size
    )


def folder_dialog(title: str) -> str:
    """调用文件管理器选择文件夹路径
    
    逻辑流程:
        打开文件夹选择对话框
        ↓
        检查用户是否选择了文件夹
        ├─ 选择了: 返回文件夹路径
        └─ 取消了: 返回空字符串

    Args:
        title: 对话框标题

    Returns:
        str: 选择的文件夹路径，如果取消则为空字符串
    """
    folder_path = filedialog.askdirectory(title=title, mustexist=True)
    if folder_path:
        return folder_path
    else:
        return ""


def write_data(data: dict) -> None:
    """写入数据到配置文件
    
    逻辑流程:
        打开数据文件 (data.json)
        ↓
        将数据字典序列化为JSON
        ↓
        写入文件 (indent=2, ensure_ascii=False)

    Args:
        data: 要写入的数据字典

    Returns:
        None
    """
    with open(path_config.DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_data() -> dict:
    """从配置文件读取数据
    
    逻辑流程:
        检查数据文件是否存在
        ├─ 不存在: 返回默认配置
        │   {
        │       "minecraft_path": "",
        │       "migrate": False
        │   }
        └─ 存在: 读取并解析JSON文件
            ↓
            返回数据字典

    Args:
        无

    Returns:
        dict: 配置数据字典，如果文件不存在则返回默认配置
    """
    if not path_config.DATA_PATH.exists():
        return data_defalut
    with open(path_config.DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    

def center_window(window:ctk.CTk|ctk.CTkToplevel):
    """让窗口居中显示
    
    逻辑流程:
        更新窗口任务以确保尺寸已计算
        ↓
        获取屏幕宽高
        ↓
        获取窗口宽高
        ↓
        计算居中位置 (x, y)
        ↓
        设置窗口位置

    Args:
        window: 窗口对象

    Returns:
        None
    """
    window.update_idletasks()
        
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    win_width = window.winfo_width()
    win_height = window.winfo_height()
    
    x = (screen_width - win_width) // 2
    y = (screen_height - win_height) // 2
    
    window.geometry(f"+{x}+{y}")
        

def auto_label_window_width(label:ctk.CTkLabel, window:ctk.CTk|ctk.CTkToplevel, window_height:int) -> None:
    """自动根据Label文字宽度设置窗口宽度
    
    逻辑流程:
        更新窗口任务以渲染Label
        ↓
        获取Label文本宽度
        ↓
        计算窗口宽度 (文本宽度 + 40)
        ↓
        设置窗口尺寸

    Args:
        label: Label组件对象
        window: 窗口对象
        window_height: 窗口高度

    Returns:
        None
    """
    window.update_idletasks()
    
    text_width = label.winfo_reqwidth()
    window.geometry(f"{text_width + 40}x{window_height}")    


def is_minecraft_folder(minecraft_path) -> dict:
    """判断是否为minecraft路径
    
    逻辑流程:
        初始化结果字典 {find: False, migrate: False}
        ↓
        检查是否存在 launcher_profiles.json
        ├─ 不存在: 返回结果 {find: False, migrate: False}
        └─ 存在: 继续检查
            ↓
            检查是否存在标准 saves 文件夹
            ├─ 存在: 设置 find=True, 返回结果
            └─ 不存在: 检查是否存在 versions 文件夹
                ├─ 存在: 设置 find=True, migrate=True, 返回结果
                └─ 不存在: 返回原始结果 {find: False, migrate: False}

    Args:
        minecraft_path: 要检查的文件夹路径

    Returns:
        dict: 包含检查结果的字典
            - find (bool): 是否为有效的.minecraft文件夹
            - migrate (bool): 是否为版本迁移结构（存档在versions目录下）
    """
    result:dict = {
        "find": False,
        "migrate": False
    }
    
    if not Path(minecraft_path, "launcher_profiles.json").exists():
        return result
    
    if Path(minecraft_path, "saves").exists():
        result["find"] = True
    elif Path(minecraft_path, "versions").exists():
        result["find"] = True
        result["migrate"] = True
        
    return result
