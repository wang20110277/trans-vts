#!/bin/bash

# 激活 trans-wsp-mcp 环境的脚本

echo "激活 trans-wsp-mcp-py310 环境..."
source ~/.zshrc
conda activate trans-wsp-mcp-py310

echo "环境已激活，当前Python版本:"
python --version

echo "已安装的包:"
pip list | grep -E "(fastmcp|mcp|flask|requests)"

echo ""
echo "现在可以运行服务:"
echo "python src/main.py"