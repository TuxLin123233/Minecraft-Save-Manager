from config import *

def zip_extract(zip_path, extract_path, name):
    """解压zip文件"""
    """
    zip_path: 压缩包路径
    extract_path: 解压路径
    """

    # 先解压到临时文件夹
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(TEMP_PATH)

    # 获取第一个文件夹
    origin_path = glob.glob(os.path.join(TEMP_PATH, '*'))[0]
    # 移动文件夹并重新命名
    shutil.move(origin_path, os.path.join(extract_path, name))

def get_image(image_name:str, size:tuple) -> ctk.CTkImage:
    """获取CtkImage(可缩放)"""
    pil_image = Image.open(os.path.join('.', 'img', f"{image_name}.png"))
    return ctk.CTkImage(
        light_image=pil_image,  # 浅色模式图片
        dark_image=pil_image,   # 深色模式图片
        size=size
    )