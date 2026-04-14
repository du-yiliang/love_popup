# 爱心祝福语动画 - 部署文档

## 项目简介

这是一个使用 Python tkinter 开发的桌面动画程序，运行后会在屏幕中央显示一个由祝福语组成的爱心形状，随后祝福语会散开并以下雨坠落效果消失。

### 功能特点

- **心形排列**：32条祝福语从屏幕随机位置汇聚成爱心形状
- **渐显动画**：文字带渐显效果，颜色随机从20种柔和彩色中选取
- **散开效果**：爱心形成后，所有文字同时快速散开
- **下雨坠落**：文字以下雨坠落的方式加速下落并逐渐消失
- **支持表情符号**：祝福语中包含丰富的 emoji 表情
- **交互退出**：按 `Esc` 键或鼠标左键点击可提前退出

---

## 系统要求

### 操作系统

- Windows 10/11 ✅（已测试）
- macOS（理论上支持，需测试）
- Linux（理论上支持，需测试）

### Python 版本

- Python 3.6 或以上版本（推荐 Python 3.8+）

### 依赖库

本项目**无需安装任何第三方库**，仅使用 Python 标准库：

| 模块 | 用途 |
|------|------|
| `tkinter` | GUI 界面框架 |
| `math` | 心形坐标计算 |
| `random` | 随机数生成 |
| `threading` | 多线程动画 |
| `time` | 时间控制 |

> ✅ tkinter 通常随 Python 官方安装包一起提供，Windows 系统默认包含。

---

## 部署方式

### 方式一：直接运行源码（推荐开发调试使用）

#### 1. 安装 Python

从 [Python 官网](https://www.python.org/downloads/) 下载并安装 Python 3.8+。

安装时**务必勾选** `Add Python to PATH` 选项。

#### 2. 验证安装

```cmd
python --version
```

应显示 `Python 3.x.x`。

#### 3. 运行程序

```cmd
python love_v3.py
```

程序将立即启动动画，全屏显示。

---

### 方式二：打包为独立 EXE 可执行文件（推荐发布给用户）

#### 1. 安装 PyInstaller

```cmd
pip install pyinstaller
```

#### 2. 打包程序

项目已提供打包配置文件 `LoveV3.spec`，直接运行：

```cmd
pyinstaller LoveV3.spec
```

或者手动打包：

```cmd
pyinstaller --onefile --noconsole --name LoveV3 love_v3.py
```

#### 3. 获取可执行文件

打包完成后，EXE 文件位于：

```
dist\LoveV3.exe
```

该文件可独立运行，**目标机器无需安装 Python**。

---

### 方式三：使用已打包的 EXE

如果 `dist\` 目录下已有 `LoveV3.exe`，直接双击运行即可。

---

## 使用说明

### 启动

- 运行 `love_v3.py` 或 `LoveV3.exe`
- 程序将自动全屏显示动画

### 动画流程

```
阶段1: 祝福语从随机位置汇聚成爱心形状（约3秒）
       ↓
阶段2: 所有文字同时快速散开，并生成更多祝福语（约4秒）
       ↓
阶段3: 文字以下雨坠落效果加速下落并消失（约3秒）
       ↓
程序自动退出
```

### 提前退出

- 按键盘 **`Esc`** 键
- 或 **鼠标左键点击** 屏幕任意位置

---

## 自定义配置

### 修改祝福语内容

编辑 `love_v3.py` 文件中的 `BLESSINGS` 列表（第 10-43 行）：

```python
BLESSINGS = [
    "别熬夜 💕",
    "多喝水 💗",
    # ... 添加或修改祝福语
    "自定义祝福语 💖",
]
```

### 修改文字颜色

编辑 `TEXT_COLORS` 列表（第 46-69 行），添加十六进制颜色值：

```python
TEXT_COLORS = [
    '#ff6b9d',  # 粉色
    '#ff8c42',  # 橙色
    # ... 添加更多颜色
]
```

### 调整动画参数

在对应的方法中修改：

| 参数 | 位置 | 说明 |
|------|------|------|
| `scale=10` | `phase_heart_formation()` 第 208 行 | 爱心大小 |
| `font_size=13` | `phase_heart_formation()` 第 219 行 | 文字大小 |
| `time.sleep(2)` | `phase_heart_formation()` 第 226 行 | 心形停留时间（秒） |
| `time.sleep(2.5)` | `phase_scatter()` 第 263 行 | 散开后停留时间（秒） |
| `speed=8` | `fall_down()` 默认参数 | 下雨下落初始速度 |

---

## 常见问题

### Q1: 运行时报错 `No module named tkinter`

**原因**：Python 安装时未包含 tkinter。

**解决方法**：
- Windows：重新安装 Python，确保勾选 `tcl/tk and IDLE`
- Linux：`sudo apt-get install python3-tk`

### Q2: 窗口不是全屏

**原因**：某些系统或多显示器环境下 tkinter 全屏行为异常。

**解决方法**：手动调整代码中的 `overrideredirect(True)` 和 `geometry()` 设置。

### Q3: 表情符号显示为方框

**原因**：系统字体不支持 emoji。

**解决方法**：
- Windows 10/11 默认支持，无需5: 更新系统字体
- 或修改 `font` 参数为支持 emoji 的字体，如 `('Segoe UI Emoji', font_size, 'bold')`

### Q4: 打包后 EXE 文件很大

**原因**：PyInstaller 会打包整个 Python 解释器。

**解决方法**：
- 使用 `--onefile` 参数合并为单个文件
- 使用 UPX 压缩：`pip install pyinstaller[encryption]`
- 这是正常现象，通常在 10-20MB

### Q5: 运行时被杀毒软件拦截

**原因**：PyInstaller 打包的 EXE 可能被误报。

**解决方法**：
- 将程序添加到杀毒软件白名单
- 或使用代码签名证书签名 EXE

---

## 项目文件说明

```
e:\qwendata\2\
├── love_v3.py          # 主程序源码（当前版本）
├── love_popup.py       # 旧版本源码
├── love_v2.py          # 旧版本源码
```

---

## 技术架构

```
HeartTextAnimation (主类)
    ├── tkinter 全屏窗口
    ├── 无边框、置顶、透明背景
    │
    └── 动画三阶段
        ├── phase_heart_formation()  → 心形排列
        ├── phase_scatter()          → 散开效果
        └── phase_fade_out()         → 下雨坠落

FloatingText (文字类)
    ├── show()        → 渐显动画
    ├── move_to()     → 平滑移动
    ├── scatter_move()→ 快速散开
    └── fall_down()   → 下雨坠落（加速+淡出）
```

---

## 版本历史

| 版本 | 说明 |
|------|------|
| V1 (love_popup.py) | 初始版本 |
| V2 (love_v2.py) | 功能增强版 |
| V3 (love_v3.py) | 当前版本，优化动画效果和颜色系统 |

---

## 许可证

本项目仅供学习交流使用。

---

## 联系方式

如有问题或建议，请联系项目维护者。
