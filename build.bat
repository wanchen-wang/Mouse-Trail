@echo off
chcp 65001 >nul
echo ============================================
echo 轨迹精灵 - 打包脚本
echo ============================================
echo.

echo 正在检查依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败！
    pause
    exit /b 1
)

echo.
echo 正在清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo 正在使用PyInstaller打包...
pyinstaller main.spec
if errorlevel 1 (
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo ============================================
echo 打包完成！
echo 可执行文件位置: dist\轨迹精灵.exe
echo ============================================
pause

