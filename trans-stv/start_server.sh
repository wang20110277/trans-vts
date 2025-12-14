#!/bin/bash

# 禁止生成 __pycache__ 文件
export PYTHONDONTWRITEBYTECODE=1

# 终止已运行的服务器进程
echo "终止已运行的服务器进程..."
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null

# 启动服务器
echo "启动阿雅语音助手服务器..."
python server.py "$@"