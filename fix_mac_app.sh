#!/bin/bash

# 快速修复Mac应用的脚本
# 使用方法：将此脚本和轨迹精灵.app放在同一目录，然后运行 ./fix_mac_app.sh

APP_NAME="轨迹精灵.app"

echo "============================================"
echo "修复Mac应用 - 移除隔离属性"
echo "============================================"
echo ""

# 检查应用是否存在
if [ ! -d "$APP_NAME" ]; then
    echo "错误：未找到 $APP_NAME"
    echo "请确保应用文件在当前目录"
    exit 1
fi

echo "正在移除隔离属性..."
xattr -cr "$APP_NAME"

if [ $? -eq 0 ]; then
    echo "✓ 成功移除隔离属性"
    echo ""
    echo "现在可以运行应用了："
    echo "  方法1: 直接双击 $APP_NAME"
    echo "  方法2: 右键点击 → 选择'打开'"
    echo "  方法3: 在终端执行: open $APP_NAME"
else
    echo "✗ 移除失败，请尝试手动执行："
    echo "  xattr -cr \"$APP_NAME\""
    exit 1
fi

echo ""
echo "============================================"
