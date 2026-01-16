import keyboard  # 用于全局热键
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSlider, QPushButton, QColorDialog, QGroupBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor


class ControlPanel(QWidget):
    """轨迹精灵 - 控制中心"""
    settings_changed = pyqtSignal(int, QColor, QColor)  # 信号：初始透明度, 起始颜色, 结束颜色
    
    def __init__(self, trail_widget):
        super().__init__()
        self.trail_widget = trail_widget
        self.init_ui()
        
        # 注册全局显示/隐藏快捷键 Ctrl+O
        keyboard.add_hotkey('ctrl+o', self.toggle_visibility)
    
    def init_ui(self):
        self.setWindowTitle("轨迹精灵 - TrailSprite")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(100, 100, 420, 480)
        
        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2C3E50, stop:1 #34495E);
                color: #ECF0F1;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ECF0F1;
                border: 2px solid #3498DB;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background: rgba(52, 73, 94, 0.6);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #3498DB;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 13px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #34495E;
                height: 8px;
                background: #34495E;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498DB, stop:1 #2980B9);
                border: 2px solid #ECF0F1;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5DADE2, stop:1 #3498DB);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498DB, stop:1 #2980B9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5DADE2, stop:1 #3498DB);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980B9, stop:1 #1F618D);
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # 标题区域
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498DB, stop:1 #2980B9);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        title_layout = QVBoxLayout()
        title_label = QLabel("✨ 轨迹精灵")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
        """)
        subtitle_label = QLabel("TrailSprite - 让鼠标轨迹更精彩")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_frame.setLayout(title_layout)
        main_layout.addWidget(title_frame)
        
        # 持续时间控制组
        duration_group = QGroupBox("⏱️ 持续时间控制")
        duration_layout = QVBoxLayout()
        duration_layout.setSpacing(12)
        
        self.alpha_label = QLabel("初始透明度: 180")
        self.alpha_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #3498DB;")
        duration_layout.addWidget(self.alpha_label)
        
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.alpha_slider.setMinimum(50)
        self.alpha_slider.setMaximum(255)
        self.alpha_slider.setValue(180)
        self.alpha_slider.valueChanged.connect(self.on_alpha_changed)
        duration_layout.addWidget(self.alpha_slider)
        
        hint_label = QLabel("💡 提示：值越大，轨迹持续时间越长")
        hint_label.setStyleSheet("font-size: 11px; color: #95A5A6; font-style: italic;")
        duration_layout.addWidget(hint_label)
        
        duration_group.setLayout(duration_layout)
        main_layout.addWidget(duration_group)
        
        # 颜色选择组
        color_group = QGroupBox("🎨 颜色渐变设置")
        color_layout = QVBoxLayout()
        color_layout.setSpacing(15)
        
        # 起始颜色
        start_color_layout = QHBoxLayout()
        start_color_layout.setSpacing(15)
        start_label = QLabel("起始颜色:")
        start_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        start_color_layout.addWidget(start_label)
        self.start_color_btn = QPushButton("选择颜色")
        self.start_color_btn.clicked.connect(self.choose_start_color)
        self.start_color_btn.setFixedSize(120, 40)
        self.start_color_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 215, 0);
                border: 2px solid #ECF0F1;
            }
            QPushButton:hover {
                border: 3px solid #ECF0F1;
            }
        """)
        start_color_layout.addWidget(self.start_color_btn)
        start_color_layout.addStretch()
        color_layout.addLayout(start_color_layout)
        
        # 结束颜色
        end_color_layout = QHBoxLayout()
        end_color_layout.setSpacing(15)
        end_label = QLabel("结束颜色:")
        end_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        end_color_layout.addWidget(end_label)
        self.end_color_btn = QPushButton("选择颜色")
        self.end_color_btn.clicked.connect(self.choose_end_color)
        self.end_color_btn.setFixedSize(120, 40)
        self.end_color_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 0, 0);
                border: 2px solid #ECF0F1;
            }
            QPushButton:hover {
                border: 3px solid #ECF0F1;
            }
        """)
        end_color_layout.addWidget(self.end_color_btn)
        end_color_layout.addStretch()
        color_layout.addLayout(end_color_layout)
        
        color_hint = QLabel("💡 轨迹会从起始颜色渐变到结束颜色")
        color_hint.setStyleSheet("font-size: 11px; color: #95A5A6; font-style: italic;")
        color_layout.addWidget(color_hint)
        
        color_group.setLayout(color_layout)
        main_layout.addWidget(color_group)
        
        # 快捷键提示
        shortcut_frame = QFrame()
        shortcut_frame.setStyleSheet("""
            QFrame {
                background: rgba(52, 73, 94, 0.5);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        shortcut_layout = QVBoxLayout()
        shortcut_title = QLabel("⌨️ 快捷键")
        shortcut_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #3498DB;")
        shortcut_layout.addWidget(shortcut_title)
        shortcut_info = QLabel("Ctrl+O: 显示/隐藏面板  |  Ctrl+P: 退出程序")
        shortcut_info.setStyleSheet("font-size: 10px; color: #95A5A6;")
        shortcut_layout.addWidget(shortcut_info)
        shortcut_frame.setLayout(shortcut_layout)
        main_layout.addWidget(shortcut_frame)
        
        # 按钮组
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.close_btn = QPushButton("隐藏面板")
        self.close_btn.setFixedSize(120, 40)
        self.close_btn.clicked.connect(self.hide)
        button_layout.addWidget(self.close_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
        # 初始化颜色
        self.start_color = QColor(255, 215, 0)
        self.end_color = QColor(255, 0, 0)
    
    def on_alpha_changed(self, value):
        """透明度滑块改变时的回调"""
        self.alpha_label.setText(f"初始透明度: {value}")
        self.apply_settings()
    
    def choose_start_color(self):
        """选择起始颜色"""
        color = QColorDialog.getColor(self.start_color, self, "选择起始颜色")
        if color.isValid():
            self.start_color = color
            self.start_color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                    border: 2px solid #ECF0F1;
                }}
                QPushButton:hover {{
                    border: 3px solid #ECF0F1;
                }}
            """)
            self.apply_settings()
    
    def choose_end_color(self):
        """选择结束颜色"""
        color = QColorDialog.getColor(self.end_color, self, "选择结束颜色")
        if color.isValid():
            self.end_color = color
            self.end_color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgb({color.red()}, {color.green()}, {color.blue()});
                    border: 2px solid #ECF0F1;
                }}
                QPushButton:hover {{
                    border: 3px solid #ECF0F1;
                }}
            """)
            self.apply_settings()
    
    def apply_settings(self):
        """应用设置到轨迹窗口"""
        if self.trail_widget:
            self.trail_widget.update_settings(
                self.alpha_slider.value(),
                self.start_color,
                self.end_color
            )
    
    def toggle_visibility(self):
        """切换控制面板显示/隐藏"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

