#!/bin/bash

# 禁止生成 __pycache__ 文件
export PYTHONDONTWRITEBYTECODE=1

# 启动主程序
echo "启动阿雅语音助手主程序..."
python main.py "$@"