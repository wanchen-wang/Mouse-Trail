import ctypes # 用于 DPI 感知设置
import keyboard  # 用于全局热键
from PyQt6.QtWidgets import QWidget # 基本窗口类
from PyQt6.QtCore import Qt, QTimer, QPoint # 基本 Qt 常量和计时器
from PyQt6.QtGui import QPainter, QColor, QCursor # 绘图和颜色处理
from PyQt6.QtGui import QPainterPath, QPolygonF # 用于自定义形状绘制
from PyQt6.QtCore import QPointF # 用于更精确的浮点坐标
from PyQt6.QtWidgets import QApplication
import math # 用于计算星形顶点        
import random

# DPI 感知设置，确保高分屏坐标精准
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)# 系统DPI感知
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()# 系统DPI感知

class MouseTrail(QWidget):
    def __init__(self, control_panel=None):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )# 设置无边框、置顶、工具窗口、透明点击穿透
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)# 设置背景透明
        self.showFullScreen()

        self.points = []
        self.last_pos = None # 用于检测静止状态
        self.control_panel = control_panel
        
        # 默认配置参数
        self.initial_alpha = 180  # 初始透明度（控制持续时间）
        self.start_color = QColor(255, 215, 0)  # 起始颜色（橙色）
        self.end_color = QColor(255, 0, 0)  # 结束颜色（红色）
        
        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_trail)
        self.timer.start(10) 

        # 注册全局退出快捷键 Ctrl+P
        keyboard.add_hotkey('ctrl+p', self.close_app)
    
    def update_settings(self, initial_alpha, start_color, end_color):
        """更新设置参数"""
        self.initial_alpha = initial_alpha
        self.start_color = start_color
        self.end_color = end_color

    def update_trail(self):
        current_global_pos = QCursor.pos()
        
        if current_global_pos != self.last_pos:
            local_pos = self.mapFromGlobal(current_global_pos)
            base_x = local_pos.x() + 10
            base_y = local_pos.y() + 10
            
            for _ in range(5): 
                vx = random.uniform(-1.5, 1.5)
                vy = random.uniform(-1.5, 1.5)
                r_size = random.randint(2, 4)
                
                # 随机选择形状：0-圆形, 1-星形, 2-六芒星
                shape_type = random.randint(0, 2) 
                
                # 存储：[位置点 (QPointF), 透明度, 大小, vx, vy, 形状类型]
                self.points.append([QPointF(base_x, base_y), self.initial_alpha, r_size, vx, vy, shape_type])
            
            self.last_pos = current_global_pos

        for p in self.points:
            # 确保使用 QPointF 的 setX 和 setY
            p[0].setX(p[0].x() + p[3])
            p[0].setY(p[0].y() + p[4])
            
            p[1] -= 2
        
        self.points = [p for p in self.points if p[1] > 0]
        self.update()

    # 辅助函数：生成星形的 QPainterPath
    def _create_star_path(self, center, outer_radius, inner_radius, num_points=5):
        path = QPainterPath()
        points = []
        for i in range(num_points * 2):
            radius = outer_radius if i % 2 == 0 else inner_radius
            angle = i * math.pi / num_points - math.pi / 2 # 调整角度使星星尖角朝上
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            points.append(QPointF(x, y))
        
        path.moveTo(points[0])
        for i in range(1, len(points)):
            path.lineTo(points[i])
        path.closeSubpath()
        return path

    # 辅助函数：生成六芒星的 QPainterPath (两个重叠的三角形)
    def _create_hexagram_path(self, center, radius):
        path = QPainterPath()
        # 第一个三角形 (尖角朝上)
        triangle1_points = []
        for i in range(3):
            angle = i * 2 * math.pi / 3 - math.pi / 2 # 调整角度
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            triangle1_points.append(QPointF(x, y))
        path.addPolygon(QPolygonF(triangle1_points))

        # 第二个三角形 (尖角朝下)
        triangle2_points = []
        for i in range(3):
            angle = i * 2 * math.pi / 3 + math.pi / 6 # 调整角度，与第一个错开
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            triangle2_points.append(QPointF(x, y))
        path.addPolygon(QPolygonF(triangle2_points))
        return path


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)#    开启抗锯齿

        for point, alpha, size, vx, vy, shape_type in self.points:
            # 计算颜色渐变：根据当前透明度在起始颜色和结束颜色之间插值
            # alpha_ratio 从 1.0 (初始) 到 0.0 (消失)
            alpha_ratio = alpha / self.initial_alpha if self.initial_alpha > 0 else 0
            
            # 线性插值计算RGB值
            r = int(self.start_color.red() * alpha_ratio + self.end_color.red() * (1 - alpha_ratio))
            g = int(self.start_color.green() * alpha_ratio + self.end_color.green() * (1 - alpha_ratio))
            b = int(self.start_color.blue() * alpha_ratio + self.end_color.blue() * (1 - alpha_ratio))
            
            color = QColor(r, g, b, alpha)
            
            painter.setBrush(color)# 设置画刷颜色
            painter.setPen(Qt.PenStyle.NoPen)
            
            # 根据形状类型绘制
            if shape_type == 0: # 圆形
                painter.drawEllipse(point, size, size)
            elif shape_type == 1: # 星形
                # outer_radius = size, inner_radius = size * 0.4
                star_path = self._create_star_path(point, size, size * 0.4) 
                painter.drawPath(star_path)
            elif shape_type == 2: # 六芒星
                hexagram_path = self._create_hexagram_path(point, size)
                painter.drawPath(hexagram_path)

    def close_app(self):
        print("程序已通过快捷键 Ctrl+P 退出")
        QApplication.quit()

