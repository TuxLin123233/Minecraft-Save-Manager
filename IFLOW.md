# iFlow 项目文档 - Minecraft 存档管理器

## 项目概述

这是一个简单好用的 Minecraft Java 版存档管理工具，提供图形化界面来管理 Minecraft 存档。主要功能包括导入 ZIP 格式的地图、导出存档备份、查看存档列表等。

**项目类型**: Python GUI 应用程序
**主要技术**: Python 3.10+, CustomTkinter, Pillow, PyInstaller
**目标平台**: Windows (通过 EXE 分发)

## 项目结构

```
存档管理器/
├── code/                      # 源代码目录
│   ├── main.py               # 程序入口
│   ├── gui.py                # GUI 界面实现
│   ├── config.py             # 配置文件
│   ├── utils.py              # 工具函数集合
│   ├── data.json             # 用户配置数据（运行时生成）
│   ├── temp/                 # 临时文件夹（运行时生成）
│   └── img/                  # 图片资源
│       ├── steve.png         # Steve 头像
│       ├── map.png           # 地图图标
│       ├── box.png           # 盒子图标（导出）
│       ├── book_pen.png      # 书本图标（列表）
│       ├── golden_apple.png  # 金苹果图标（赞助）
│       └── screenshot.png    # 截图
├── icon.ico                   # 应用程序图标
├── requirements.txt           # Python 依赖列表
├── README.md                  # 项目说明文档
└── .github/workflows/
    └── build-exe.yml          # GitHub Actions 自动构建配置
```

## 核心架构

### 代码组织

**main.py** - 应用入口
- 初始化应用程序
- 启动 GUI 主循环

**gui.py** - 用户界面层
- `App` 类：主应用程序类
- `create_header()`: 创建标题栏（含 Steve 图标和标题）
- `create_buttons()`: 创建功能按钮（2x2 网格布局）
- `import_save()`: 导入存档功能实现
- `progress_window()`: 创建进度条窗口
- 使用 CustomTkinter 构建现代化 UI

**config.py** - 配置层
- 定义基础路径常量
- BASE_DIR: 代码目录路径
- TEMP_PATH: 临时文件夹路径
- DATA_PATH: 配置文件路径

**utils.py** - 工具函数层
- `zip_extract()`: 解压 ZIP 文件并移动到目标位置
- `get_image()`: 加载并缩放 PNG 图片为 CTkImage
- `foder_dialog()`: 调用文件对话框选择文件夹
- `write_data()`: 写入 JSON 配置文件
- `read_data()`: 读取 JSON 配置文件

### 数据流

1. **用户配置**: 存储在 `code/data.json`，包含 minecraft_path 等设置
2. **临时文件**: 解压时使用 `code/temp/` 作为中间目录
3. **图片资源**: 运行时动态加载 `code/img/` 中的 PNG 文件

## 核心功能

### 1. 导入存档

**流程**:
1. 检查是否已记录 .minecraft 文件夹路径
2. 如果未记录，提示用户选择 .minecraft 文件夹
3. 选择存放 ZIP 地图的文件夹
4. 遍历文件夹中的所有 ZIP 文件
5. 解压每个 ZIP 到临时目录
6. 移动解压后的文件夹到 `.minecraft/saves`
7. 显示进度条和完成提示

**技术要点**:
- 使用 zipfile 模块解压
- 使用 glob 查找所有 ZIP 文件
- 使用 shutil.move 移动文件夹
- 实时更新进度条

### 2. 导出存档

- 打包现有存档为 ZIP 格式
- 支持批量导出

### 3. 存档列表

- 显示所有已安装的存档
- 提供存档管理功能

### 4. 赞助功能

- 提供赞助链接

## 依赖管理

### 核心依赖

```txt
customtkinter==5.2.2    # 现代化 GUI 框架
pillow==12.1.1          # 图像处理
darkdetect==0.8.0       # 主题检测
packaging==26.0         # 打包工具
```

### 开发依赖

```txt
pyinstaller==6.19.0                    # 打包成 EXE
pyinstaller-hooks-contrib==2026.2     # PyInstaller 钩子
setuptools==82.0.0                      # 构建工具
```

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/TuxLin123233/Python-EXE.git
cd 存档管理器
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行程序

```bash
cd code
python main.py
```

## 构建与打包

### 本地打包

在项目根目录执行：

```bash
# 进入代码目录
cd code

# 打包命令
pyinstaller -F --icon="../icon.ico" --name="存档管理器" --add-data="img;img" main.py

# 输出文件在 dist/存档管理器.exe
```

**打包参数说明**:
- `-F`: 单文件模式
- `--icon`: 设置图标
- `--name`: 设置输出文件名
- `--add-data`: 打包图片资源
- `--noconsole`: 不显示控制台窗口（生产环境）

### 自动构建

项目配置了 GitHub Actions，在推送到 `main` 分支时自动构建：

**触发条件**:
- 推送到 `main` 分支
- 手动触发 (workflow_dispatch)

**构建环境**:
- Windows-latest
- Python 3.10

**构建流程**:
1. 检出代码
2. 设置 Python 环境
3. 安装依赖
4. 使用 PyInstaller 打包
5. 上传构建产物

**产物位置**: GitHub Actions Artifacts - `SaveManager-Windows`

## 代码规范

### 命名约定

- **类名**: 大驼峰 (PascalCase) - `App`
- **函数名**: 小写下划线 (snake_case) - `import_save`
- **变量名**: 小写下划线 (snake_case) - `minecraft_path`
- **常量**: 大写下划线 (UPPER_SNAKE) - `BASE_DIR`

### 文档风格

- 使用 Google 风格的 docstring
- 函数包含 Args 和 Returns 说明
- 关键逻辑添加行内注释

### 导入顺序

1. 标准库
2. 第三方库
3. 本地模块

## 开发实践

### 调试技巧

1. **查看 GUI 事件**: 在回调函数中添加 print 语句
2. **测试文件操作**: 使用 temp 目录进行测试
3. **进度条调试**: 在 progress_window 中添加日志

### 常见问题

**Q: 图片无法加载？**
A: 检查 `code/img/` 目录下是否有对应的 PNG 文件

**Q: .minecraft 路径未保存？**
A: 检查 `code/data.json` 文件权限和内容

**Q: 打包后图片不显示？**
A: 确保使用 `--add-data="img;img"` 参数打包

### 扩展功能建议

- [ ] 添加存档预览功能（读取 level.dat）
- [ ] 支持存档版本控制
- [ ] 添加自动备份功能
- [ ] 支持多语言界面
- [ ] 添加存档搜索和过滤功能

## Git 工作流

### 分支策略

- `main`: 主分支，稳定版本
- 开发在 `main` 分支直接进行

### 提交规范

```
优化路径配置
小修改
隐藏终端
小更新
修复PowerShell语法
```

### 忽略文件

已配置 `.gitignore`:
- Python 虚拟环境 (`.venv/`)
- Python 缓存 (`__pycache__/`, `*.pyc`)
- 打包文件 (`dist/`, `build/`)
- IDE 配置 (`.vscode/`, `.idea/`)
- 系统文件 (`.DS_Store`, `Thumbs.db`)

## 部署流程

### 发布新版本

1. 更新版本号（如果需要）
2. 更新 README.md 中的下载链接
3. 推送到 GitHub
4. 等待 GitHub Actions 完成构建
5. 从 Actions Artifacts 下载 EXE
6. 上传到 GitHub Releases

### 分发方式

- GitHub Releases 提供最新版本下载
- EXE 文件包含所有依赖，无需额外安装

## 维护指南

### 更新依赖

```bash
pip list --outdated
pip install --upgrade <package-name>
pip freeze > requirements.txt
```

### 代码审查要点

1. 检查文件路径处理是否跨平台兼容
2. 验证错误处理是否完善
3. 确保用户配置正确保存和读取
4. 测试打包后的 EXE 功能

### 性能优化

- 大文件解压时显示进度
- 避免重复加载图片资源
- 使用生成器处理大量文件

## 许可证

MIT License © 2026 TuxLin123233

## 联系方式

- GitHub: https://github.com/TuxLin123233/Minecraft-Save-Manager
- Issues: 通过 GitHub Issues 提交问题

---

**最后更新**: 2026-03-07
**文档版本**: 1.0