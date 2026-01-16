#!/bin/bash

echo "============================================"
echo "轨迹精灵 - 打包脚本 (Linux/Mac)"
echo "============================================"
echo ""

echo "正在检查依赖..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "依赖安装失败！"
    exit 1
fi

echo ""
echo "正在清理旧的构建文件..."
rm -rf build dist __pycache__

echo ""
echo "正在使用PyInstaller打包..."
pyinstaller main.spec
if [ $? -ne 0 ]; then
    echo "打包失败！"
    exit 1
fi

echo ""
echo "============================================"
echo "打包完成！"
echo "可执行文件位置: dist/轨迹精灵"
echo "============================================"

