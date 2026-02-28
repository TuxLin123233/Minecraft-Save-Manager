import os
import zipfile
import glob


TEMP_PATH = os.path.join('.', 'temp')

"""with open("./data.json", encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
"""

def zip_extract(zip_path, extract_path, name):
    """解压zip文件"""
    """
    zip_path: 压缩包路径
    extract_path: 解压路径
    """

    # 先解压到临时文件夹
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(TEMP_PATH)

    # 获取原始文件(名)路径
    origin_path = os.path.join(glob.glob(os.path.join(TEMP_PATH, '*\\'))[0])
    # 去掉某尾反斜杠
    origin_path = origin_path.rstrip('\\/')
    
    os.system(f'move "{origin_path}" "{os.path.join(extract_path, name)}"')

class Box:
    def __init__(self):
        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)
    
    def move_saves(self):
        """移动存档"""
        from_path = input("粘贴你下载好的地图文件夹路径：")
        to_path = input("粘贴.minecraft文件夹路径: ")
        # 获取所有zip的迭代器
        zip_files = glob.glob(os.path.join(from_path, "*.zip"))
        to_path = os.path.join(to_path, 'saves')
        # 进行逐个解压
        for i in zip_files:
            # 获取每个zip文件的路径
            zip_path = os.path.join(i)  
            # 获取zip文件名
            name = os.path.splitext(os.path.basename(i))[0]
            # 执行解压操作
            zip_extract(zip_path=zip_path, extract_path=to_path, name=name)
            print(f"存档: {name} 解压完成!")

box = Box()


print("""
==============================
欢迎使用小林工具箱!
输入menu查看菜单, 输入exit退出程序
==============================""")

def menu():
    menu = {
            'menu': "查看菜单",
            'exit': "退出脚本",
            '1':"执行存档批量导入"
        }
    for i,v in menu.items():
        print(i, v)

menu()
while True:
    user = input("=> ")
    if user == "menu":
        menu()
    elif user == 'exit':
        os.system("pause")
        break
    elif user == '1':
        box.move_saves()
    