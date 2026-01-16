#!/bin/bash

echo "============================================"
echo "轨迹精灵 - Mac打包脚本"
echo "============================================"
echo ""

# 检查是否在Mac上
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "错误：此脚本只能在macOS上运行！"
    exit 1
fi

echo "正在检查依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "依赖安装失败！"
    exit 1
fi

echo ""
echo "正在清理旧的构建文件..."
rm -rf build dist __pycache__

echo ""
echo "正在使用PyInstaller打包Mac应用..."
pyinstaller main_mac.spec
if [ $? -ne 0 ]; then
    echo "打包失败！"
    exit 1
fi

echo ""
echo "正在移除隔离属性（解决Gatekeeper问题）..."
if [ -d "dist/轨迹精灵.app" ]; then
    xattr -cr "dist/轨迹精灵.app"
    echo "✓ 已移除隔离属性"
else
    echo "警告：未找到应用文件"
fi

echo ""
echo "============================================"
echo "打包完成！"
echo "应用位置: dist/轨迹精灵.app"
echo ""
echo "⚠️  重要提示："
echo "1. 首次运行可能需要右键点击应用，选择'打开'"
echo "2. 如果仍然无法运行，请在终端执行："
echo "   xattr -cr dist/轨迹精灵.app"
echo "3. 或者前往：系统设置 > 隐私与安全性"
echo "   允许运行未签名的应用"
echo "============================================"
