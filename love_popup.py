import tkinter as tk
from tkinter import messagebox
import threading
import time
import math
import random
import ctypes
from ctypes import wintypes

# 含蓄的表白情话
LOVE_MESSAGES = [
    "今天的天气真好,\n想和你一起去散步",
    "你喜欢的歌,\n我听了很久",
    "不知道为什么,\n看到你就觉得开心",
    "你推荐的那本书,\n我读完了",
    "今天的晚霞很好看,\n你那边也是吗?",
    "我又去了那家咖啡店,\n你坐过的位置还在",
    "今天发生了一件有趣的事,\n第一个想告诉你",
    "你说过的那句话,\n我一直记得",
    "今天的月亮很圆,\n想起你说的嫦娥奔月",
    "路过花店,\n向日葵开得正好",
    "今天的风很温柔,\n像你一样",
    "那家餐厅出了新菜品,\n要不要一起去试试?",
    "下雨了,\n你带伞了吗?",
    "今天的星星很多,\n像你说的那片星空",
    "我学会做那道菜了,\n下次做给你吃",
    "今天的阳光很灿烂,\n适合晒被子",
    "路上遇到一只小猫,\n很像你养的那只",
    "今天的晚风很舒服,\n适合散步",
    "我发现了一家小书店,\n你可能会喜欢",
    "今天的早市很热闹,\n想起你说喜欢烟火气"
]

WINDOW_TITLES = [
    "系统提示",
    "温馨提示",
    "消息通知",
    "友情提示",
    "重要提醒",
    "日程提醒",
    "备忘录",
    "通知中心"
]

# Windows API
user32 = ctypes.windll.user32

class ModernPopup(tk.Toplevel):
    """现代化毛玻璃弹窗"""
    def __init__(self, parent, title, message, x, y, width=280, height=150, is_final=False):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.resizable(False, False)
        self.overrideredirect(True)  # 无边框窗口
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.0)  # 初始透明
        self.configure(bg='#ffffff')
        
        # 阴影效果
        self.shadow = tk.Toplevel(self)
        self.shadow.overrideredirect(True)
        self.shadow.attributes('-topmost', False)
        self.shadow.attributes('-alpha', 0.12)
        self.shadow.configure(bg='#000000')
        self.shadow.geometry(f"{width+8}x{height+8}+{int(x)-4}+{int(y)-4}")
        
        self._create_ui(title, message, is_final)
        self._animate_show()
        
    def _create_ui(self, title, message, is_final):
        # 标题栏 - 粉色渐变
        title_frame = tk.Frame(self, bg='#ff6b9d', height=28)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        # 标题文字
        tk.Label(
            title_frame,
            text=f"💖 {title}",
            bg='#ff6b9d',
            fg='white',
            font=('Microsoft YaHei', 9, 'bold'),
            anchor='w'
        ).pack(fill='both', expand=True, padx=8, side='left')
        
        # 关闭按钮
        close_btn = tk.Label(
            title_frame,
            text="✕",
            bg='#ff6b9d',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        )
        close_btn.pack(side='right', padx=4)
        close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#ff4785'))
        close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#ff6b9d'))
        close_btn.bind('<Button-1>', lambda e: self._animate_hide())
        
        # 内容区
        content_frame = tk.Frame(self, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=12, pady=10)
        
        # 爱心图标
        tk.Label(
            content_frame,
            text="💝",
            font=('Segoe UI Emoji', 28),
            bg='#ffffff'
        ).pack(side='left', padx=(0, 10))
        
        # 消息文字
        tk.Label(
            content_frame,
            text=message,
            bg='#ffffff',
            fg='#4a4a4a',
            font=('Microsoft YaHei', 10),
            justify='left',
            anchor='w'
        ).pack(side='left', fill='both', expand=True)
        
        # 按钮区
        button_frame = tk.Frame(self, bg='#ffffff')
        button_frame.pack(fill='x', pady=(0, 10))
        
        if is_final:
            # 拒绝按钮
            self._create_btn(button_frame, "让我想想", '#f8f8f8', '#666', '#f0f0f0', 
                           False).pack(side='left', padx=(30, 8), expand=True)
            # 接受按钮
            self._create_btn(button_frame, "好呀 ☺️", '#ff6b9d', 'white', '#ff4785', 
                           True).pack(side='left', padx=(8, 30), expand=True)
        else:
            self._create_btn(button_frame, "确定", '#ff6b9d', 'white', '#ff4785', 
                           True).pack(pady=5, padx=30, expand=True)
    
    def _create_btn(self, parent, text, bg, fg, hover_bg, primary):
        btn = tk.Label(
            parent,
            text=text,
            bg=bg,
            fg=fg,
            font=('Microsoft YaHei', 9, 'bold' if primary else 'normal'),
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=6
        )
        btn.bind('<Enter>', lambda e: btn.configure(bg=hover_bg))
        btn.bind('<Leave>', lambda e: btn.configure(bg=bg))
        btn.bind('<Button-1>', lambda e: self._animate_hide())
        return btn
    
    def _animate_show(self):
        """淡入动画"""
        for alpha in range(0, 105, 8):
            self.attributes('-alpha', min(1.0, alpha / 100))
            self.shadow.attributes('-alpha', min(0.12, alpha / 100 * 0.12))
            self.update()
            time.sleep(0.008)
    
    def _animate_hide(self):
        """淡出动画"""
        for alpha in range(100, -5, -8):
            a = max(0, alpha / 100)
            self.attributes('-alpha', a)
            self.shadow.attributes('-alpha', a * 0.12)
            self.update()
            time.sleep(0.008)
        self.destroy()
        try:
            self.shadow.destroy()
        except:
            pass

class LovePopupApp:
    def __init__(self, root):
        self.popups = []
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.root = root
        self.running = True

    def create_popup(self, title, message, x, y, is_final=False):
        """创建现代化弹窗"""
        if not self.running:
            return None
        
        # 确保坐标在屏幕范围内
        x = max(0, min(x, self.screen_width - 280))
        y = max(0, min(y, self.screen_height - 150))
        
        popup = ModernPopup(
            self.root, 
            title, 
            message, 
            x, y, 
            width=280, 
            height=150,
            is_final=is_final
        )
        self.popups.append(popup)
        return popup

    def phase1_initial_popup(self):
        """阶段1: 初始弹窗"""
        if not self.running:
            return
        x = (self.screen_width - 280) // 2
        y = (self.screen_height - 150) // 2

        self.create_popup(
            "系统提示",
            "今天天气不错,\n适合出去走走...顺便一起吗?",
            x, y
        )

    def phase2_heart_formation(self):
        """阶段2: 心形组合"""
        if not self.running:
            return

        center_x = self.screen_width // 2
        center_y = self.screen_height // 2

        heart_points = []
        scale = 8  # 更紧凑的比例

        # 计算完整心形 - 20个点均匀分布
        for i in range(20):
            # 从0到2π均匀分布，确保完整心形
            t = math.pi * 2 * i / 20
            x = 16 * math.pow(math.sin(t), 3)
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 
                  2 * math.cos(3*t) - math.cos(4*t))
            heart_points.append({
                'x': center_x + x * scale - 140,
                'y': center_y + y * scale - 75
            })

        # 按顺序创建心形弹窗，每个消息对应心形上的一个点
        for i, point in enumerate(heart_points):
            if not self.running:
                break
            if i < len(LOVE_MESSAGES):
                title = WINDOW_TITLES[i % len(WINDOW_TITLES)]
                self.create_popup(
                    title,
                    LOVE_MESSAGES[i],
                    point['x'],
                    point['y']
                )
                time.sleep(0.15)  # 控制出现速度

    def phase3_full_screen(self):
        """阶段3: 满屏弹窗"""
        if not self.running:
            return
            
        for _ in range(30):
            if not self.running:
                break
            time.sleep(0.12)
            x = random.randint(10, self.screen_width - 290)
            y = random.randint(10, self.screen_height - 160)
            message = random.choice(LOVE_MESSAGES)
            title = random.choice(WINDOW_TITLES)
            self.create_popup(title, message, x, y)

    def phase4_disappear(self):
        """阶段4: 逐个消失"""
        for popup in self.popups[:]:
            if not self.running:
                break
            time.sleep(0.1)
            try:
                if popup.winfo_exists():
                    popup._animate_hide()
            except:
                pass

        # 清空列表
        self.popups.clear()

    def show_final_message(self):
        """显示最终消息"""
        if not self.running:
            return
            
        x = (self.screen_width - 300) // 2
        y = (self.screen_height - 160) // 2

        popup = self.create_popup(
            "重要提示",
            "能认识你,真的很幸运。\n以后的日子,也想一直和你分享\n生活中的小确幸,可以吗?",
            x, y,
            is_final=True
        )
        
        # 最终弹窗也自动消失
        if popup:
            time.sleep(5)
            try:
                if popup.winfo_exists():
                    popup._animate_hide()
            except:
                pass

    def start_animation(self):
        """开始动画"""
        try:
            # 阶段1: 初始弹窗
            self.phase1_initial_popup()
            time.sleep(2)
            
            if not self.running:
                return
                
            # 阶段2: 心形组合
            self.phase2_heart_formation()
            time.sleep(1.5)
            
            if not self.running:
                return
                
            # 阶段3: 满屏弹窗
            self.phase3_full_screen()
            
            # 等待2秒后开始消失
            time.sleep(2)
            
            if not self.running:
                return
                
            # 阶段4: 逐个消失
            self.phase4_disappear()
            
            # 显示最终消息
            time.sleep(0.5)
            if self.running:
                self.show_final_message()
                
        except Exception as e:
            print(f"Animation error: {e}")
        finally:
            # 动画结束后退出
            time.sleep(6)
            self.running = False
            try:
                self.root.destroy()
            except:
                pass


def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    app = LovePopupApp(root)
    
    # 直接开始动画，不需要点击
    def start_thread():
        time.sleep(0.5)
        app.start_animation()
    
    threading.Thread(target=start_thread, daemon=True).start()
    
    root.mainloop()


if __name__ == "__main__":
    main()
