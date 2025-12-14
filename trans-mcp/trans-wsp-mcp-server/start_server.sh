#!/bin/bash

# trans-wsp-mcp-server 启动脚本

# 检查是否已安装依赖
if [ ! -f "venv/bin/activate" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt

echo "启动服务..."
python src/main.py 8000