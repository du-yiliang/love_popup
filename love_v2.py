import tkinter as tk
import math
import random
import threading
import time

# 简短祝福语
BLESSINGS = [
    "别熬夜 💕",
    "多喝水 💗",
    "多运动 💖",
    "按时吃饭 🍚",
    "早点休息 🌙",
    "注意保暖 🧣",
    "开心每一天 😊",
    "照顾好自己 💝",
    "少看手机 📱",
    "多晒太阳 ☀️",
    "保持微笑 😄",
    "注意身体 💕",
    "适当休息 😴",
    "喝热水哦 🍵",
    "别太累了 💗",
    "天冷加衣 🧥",
    "记得吃早饭 🥐",
    "早睡早起 🌅",
    "多散步 🚶",
    "放松心情 🎵",
    "做自己喜欢的事 💖",
    "别想太多 🍃",
    "好好爱自己 💕",
    "每天都要开心 😊",
    "注意护眼 👀",
    "伸个懒腰 🙆",
    "深呼吸 💨",
    "起来走走 🚶‍♀️",
    "喝杯温水 🥛",
    "吃个水果 🍎",
    "活动活动筋骨 💪",
    "笑一笑 😄"
]

class FloatingText:
    """漂浮文字类"""
    def __init__(self, canvas, text, x, y, font_size=14, screen_height=1080):
        self.canvas = canvas
        self.text = text
        self.current_x = x
        self.current_y = y
        self.font_size = font_size
        self.opacity = 0.0
        self.is_alive = True
        self.screen_height = screen_height  # 保存屏幕高度
        
        # 创建文字（直接带表情）
        self.text_id = canvas.create_text(
            x, y,
            text=text,
            font=('Microsoft YaHei', font_size, 'bold'),
            fill='#ff6b9d',
            state='hidden'
        )
    
    def show(self, delay=0):
        """显示文字 - 渐显"""
        time.sleep(delay)
        # 淡入动画
        for alpha in range(0, 105, 8):
            if not self.is_alive:
                break
            a = min(1.0, alpha / 100)
            color = self._blend_color('#ff6b9d', a)
            self.canvas.itemconfig(self.text_id, state='normal', fill=color)
            self.canvas.update()
            time.sleep(0.008)
        self.opacity = 1.0
    
    def move_to(self, x, y, duration=0.3):
        """移动到新位置"""
        steps = max(int(duration * 60), 10)
        dx = (x - self.current_x) / steps
        dy = (y - self.current_y) / steps
        
        for _ in range(steps):
            if not self.is_alive:
                break
            self.current_x += dx
            self.current_y += dy
            
            self.canvas.move(self.text_id, dx, dy)
            self.canvas.update()
            time.sleep(duration / steps)
    
    def scatter_move(self, x, y, duration=0.4):
        """快速散开移动"""
        steps = max(int(duration * 40), 8)
        dx = (x - self.current_x) / steps
        dy = (y - self.current_y) / steps
        
        for _ in range(steps):
            if not self.is_alive:
                break
            self.current_x += dx
            self.current_y += dy
            
            self.canvas.move(self.text_id, dx, dy)
            self.canvas.update()
            time.sleep(duration / steps)
    
    def fall_down(self, speed=8, fade_start=0.3):
        """下雨坠落效果 - 加速下落并逐渐消失"""
        # 随机左右偏移，像雨滴一样自然
        drift_x = random.uniform(-2, 2)
        
        # 加速下落参数
        acceleration = 0.3
        current_speed = speed
        
        while self.is_alive:
            # 更新位置
            self.current_y += current_speed
            self.current_x += drift_x
            
            self.canvas.move(self.text_id, drift_x, current_speed)
            
            # 计算下落进度（0-1）
            progress = (self.current_y - self.canvas.coords(self.text_id)[1] + 100) / (self.screen_height + 100)
            progress = min(1.0, progress)
            
            # 接近底部时开始淡出
            if self.current_y > self.screen_height * fade_start:
                alpha = 1.0 - ((self.current_y - self.screen_height * fade_start) / 
                              (self.screen_height * (1 - fade_start)))
                alpha = max(0, alpha)
                color = self._blend_color('#ff6b9d', alpha)
                self.canvas.itemconfig(self.text_id, fill=color)
            
            self.canvas.update()
            time.sleep(0.016)  # 约60fps
            
            # 加速
            current_speed += acceleration
            
            # 超出屏幕底部则销毁
            if self.current_y > self.screen_height + 50:
                self.is_alive = False
                break
    
    def destroy(self):
        """销毁元素"""
        try:
            self.canvas.delete(self.text_id)
        except:
            pass
    
    def _blend_color(self, hex_color, alpha):
        """混合颜色与透明度"""
        alpha = max(0, min(1, alpha))
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = int(r * alpha + 255 * (1 - alpha))
        g = int(g * alpha + 255 * (1 - alpha))
        b = int(b * alpha + 255 * (1 - alpha))
        return f'#{r:02x}{g:02x}{b:02x}'


class HeartTextAnimation:
    """心形文字动画主类"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('')
        self.root.overrideredirect(True)  # 无边框
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', '#000000')
        self.root.configure(bg='#000000')
        
        # 全屏
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.screen_width}x{self.screen_height}+0+0')
        
        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.bubbles = []
        self.running = True
        
        # 绑定退出
        self.root.bind('<Escape>', lambda e: self.stop())
        self.root.bind('<Button-1>', lambda e: self.stop())
    
    def get_heart_points(self, num_points, scale=12):
        """获取心形坐标点"""
        points = []
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        for i in range(num_points):
            t = math.pi * 2 * i / num_points
            x = 16 * math.pow(math.sin(t), 3)
            y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 
                  2 * math.cos(3*t) - math.cos(4*t))
            
            points.append({
                'x': center_x + x * scale,
                'y': center_y + y * scale - 50
            })
        
        return points
    
    def phase_heart_formation(self):
        """阶段1：心形排列"""
        num_texts = min(len(BLESSINGS), 32)
        heart_points = self.get_heart_points(num_texts, scale=10)
        
        # 随机打乱祝福语顺序
        shuffled_blessings = random.sample(BLESSINGS, num_texts)
        
        # 依次创建文字并移动到心形位置
        for i, (text, point) in enumerate(zip(shuffled_blessings, heart_points)):
            if not self.running:
                break
            
            # 在随机位置创建
            start_x = random.randint(50, self.screen_width - 50)
            start_y = random.randint(50, self.screen_height - 50)
            
            ft = FloatingText(self.canvas, text, start_x, start_y, font_size=13, 
                            screen_height=self.screen_height)
            self.bubbles.append(ft)
            
            # 显示并移动到心形位置
            ft.show(delay=0.02)
            ft.move_to(point['x'], point['y'], duration=0.3)
            
            time.sleep(0.08)
        
        # 停留一会儿
        time.sleep(2)
    
    def phase_scatter(self):
        """阶段2：全部同时散开"""
        # 所有文字同时快速散开
        scatter_targets = []
        for ft in self.bubbles:
            if not self.running:
                break
            scatter_x = random.randint(50, self.screen_width - 50)
            scatter_y = random.randint(50, self.screen_height - 50)
            scatter_targets.append((ft, scatter_x, scatter_y))
        
        # 同时启动所有移动（用线程）
        threads = []
        for ft, x, y in scatter_targets:
            t = threading.Thread(target=ft.scatter_move, args=(x, y, 0.5), daemon=True)
            threads.append(t)
            t.start()
            time.sleep(0.02)  # 极小的间隔
        
        # 等待所有移动完成
        for t in threads:
            t.join()
        
        # 继续生成更多文字
        for _ in range(25):
            if not self.running:
                break
            
            text = random.choice(BLESSINGS)
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(50, self.screen_height - 50)
            
            ft = FloatingText(self.canvas, text, x, y, font_size=12,
                            screen_height=self.screen_height)
            self.bubbles.append(ft)
            ft.show(delay=0.02)
            
            time.sleep(0.1)
        
        # 停留2-3秒
        time.sleep(2.5)
    
    def phase_fade_out(self):
        """阶段3：下雨坠落效果消失"""
        # 给每个文字随机初始速度，像雨滴一样
        for ft in self.bubbles:
            ft.fall_velocity = random.uniform(6, 12)  # 随机速度
        
        # 所有文字同时开始坠落
        threads = []
        for ft in self.bubbles:
            if not self.running:
                break
            t = threading.Thread(target=ft.fall_down, 
                               args=(ft.fall_velocity, 0.3), 
                               daemon=True)
            threads.append(t)
            t.start()
            time.sleep(0.02)  # 微小的间隔
        
        # 等待所有消失完成
        for t in threads:
            t.join()
        
        # 清理
        for ft in self.bubbles:
            ft.destroy()
        self.bubbles.clear()
    
    def start(self):
        """开始动画"""
        def run():
            try:
                # 阶段1：心形
                self.phase_heart_formation()
                
                if not self.running:
                    return
                
                # 阶段2：散开
                self.phase_scatter()
                
                if not self.running:
                    return
                
                # 阶段3：消失
                self.phase_fade_out()
                
                # 结束后退出
                time.sleep(1)
                self.stop()
                
            except Exception as e:
                print(f"Animation error: {e}")
                self.stop()
        
        # 延迟启动
        threading.Thread(target=run, daemon=True).start()
        self.root.mainloop()
    
    def stop(self):
        """停止并清理"""
        self.running = False
        
        # 清理所有文字
        for ft in self.bubbles:
            ft.destroy()
        self.bubbles.clear()
        
        try:
            self.root.destroy()
        except:
            pass


def main():
    app = HeartTextAnimation()
    app.start()


if __name__ == "__main__":
    main()
