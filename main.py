import sys
from PyQt6.QtWidgets import QApplication
from mouse_trail import MouseTrail
from control_panel import ControlPanel


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建轨迹窗口
    trail = MouseTrail()
    
    # 创建控制面板
    control_panel = ControlPanel(trail)
    trail.control_panel = control_panel
    
    # 显示控制面板
    control_panel.show()
    
    sys.exit(app.exec())