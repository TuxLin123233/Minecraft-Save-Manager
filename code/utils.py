from config import *


def zip_extract(zip_path: str, extract_path: str, name: str):
    """解压文件夹

    Args:
        zip_path (str): 该压缩包路径
        extract_path (str): 解压到的文件夹的路径
        name (str): 存档名(和zip文件的名一样)
    """

    if not os.path.exists(TEMP_PATH):  # 如果没有./temp文件夹
        os.makedirs(TEMP_PATH)

    # 先解压到临时文件夹
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(TEMP_PATH)

    # 获取第一个文件夹
    origin_path = glob.glob(os.path.join(TEMP_PATH, "*"))[0]
    # 移动文件夹并重新命名
    shutil.move(origin_path, os.path.join(extract_path, name))


def get_image(image_name: str, size: tuple) -> ctk.CTkImage:
    """获取CtkImage(可缩放)

    Args:
        image_name (str): img文件夹里面的png名
        size (tuple): 设置图片大小(元祖)

    Returns:
        ctk.CTkImage: 返回CTkImage
    """

    pil_image = Image.open(os.path.join(os.path.dirname(__file__), "img", f"{image_name}.png"))

    return ctk.CTkImage(
        light_image=pil_image, dark_image=pil_image, size=size  # 浅色模式图片  # 深色模式图片
    )


def foder_dialog(title) -> str:
    """调用文件管理器获取文件夹路径

    Args:
        title (_type_): 标题

    Returns:
        str: 文件夹路径
    """
    folder_path = filedialog.askdirectory(title=title, mustexist=True)
    return folder_path


def write_data(data: dict):
    """写入存储文件

    Args:
        data (dict): 写入的内容
    """
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_data() -> dict:
    """读取存储文件

    Returns:
        dict: 返回字典
    """
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
