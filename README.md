# Minecraft存档管理器

一个简单易用的 Minecraft 存档管理工具。

---

## 功能特点

- **批量导入**：一键导入多个地图存档
- **自动解压**：自动解压 ZIP 文件到正确位置
- **智能命名**：自动识别存档名称
- **程序图标**：精美的自定义图标
- **交互菜单**：简单明了的命令行界面

---

## 下载安装

1. 前往 [Releases](https://github.com/TuxLin123233/Python-EXE/releases) 页面
2. 下载最新的 `XiaoLinToolbox-Windows.zip`
3. 解压到任意文件夹
4. 双击运行 `XiaoLinToolbox.exe`

---

## 操作步骤

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 输入 `menu` | 查看所有可用命令 |
| 2 | 输入 `save_move` | 开始导入存档 |
| 3 | 粘贴地图文件夹路径 | 存放 ZIP 文件的文件夹 |
| 4 | 粘贴 .minecraft 路径 | Minecraft 游戏目录 |
| 5 | 等待完成 | 自动解压并移动 |

---

## 系统要求

- Windows 7/8/10/11
- 无需安装 Python
- 无需网络连接

---

## 文件说明
├── XiaoLinToolbox.exe # 主程序

└── temp/ # 临时文件夹（自动创建）

---

---

## 常见问题

**Q: 为什么提示“找不到该功能”？**  
A: 请输入正确的命令，输入 `menu` 查看可用功能。

**Q: 存档导入到哪里了？**  
A: 导入到 `.minecraft/saves/` 文件夹，所有版本的 Minecraft 都能识别。

**Q: 如何更新到最新版？**  
A: 重新下载最新的 `XiaoLinToolbox-Windows.zip` 替换旧文件即可。

---

## 更新日志

**v1.5**
- 添加交互菜单
- 美化界面显示
- 修复路径空格问题

**v1.0**
- 首次发布
- 支持批量导入存档

---

## 关于项目

- GitHub: [TuxLin123233/Python-EXE](https://github.com/TuxLin123233/Python-EXE)
- 作者: [@TuxLin123233](https://github.com/TuxLin123233)
- 许可证: MIT

如果觉得好用，欢迎给个 ⭐！
