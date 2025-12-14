#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
财富管理查询服务主程序
使用MCP SDK提供财富相关的查询接口
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import app

if __name__ == "__main__":
    # 默认端口8000，可以通过命令行参数指定
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    app.run(host="0.0.0.0", port=port, debug=True)