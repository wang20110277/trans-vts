#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试FastMCP财富查询服务的脚本
"""

import requests
import json

def test_mcp_list_tools():
    """测试列出工具功能"""
    try:
        # 发送list_tools请求
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 1
        }
        
        response = requests.post(
            "http://localhost:8000/mcp", 
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )
        
        print("List Tools:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"List tools test failed: {e}")
        print()

def test_query_financial_products():
    """测试查询金融产品功能"""
    try:
        # 发送call_tool请求
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "query_financial_products",
                "arguments": {
                    "risk_level": "低"
                }
            },
            "id": 2
        }
        
        response = requests.post(
            "http://localhost:8000/mcp", 
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )
        
        print("Query Financial Products (Low Risk):")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"Query financial products test failed: {e}")
        print()

def test_list_resources():
    """测试列出资源功能"""
    try:
        # 发送list_resources请求
        payload = {
            "jsonrpc": "2.0",
            "method": "resources/list",
            "params": {},
            "id": 3
        }
        
        response = requests.post(
            "http://localhost:8000/mcp", 
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )
        
        print("List Resources:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
    except Exception as e:
        print(f"List resources test failed: {e}")
        print()

if __name__ == "__main__":
    print("Testing FastMCP Wealth Query Service\n")
    
    # 测试列出工具
    test_mcp_list_tools()
    
    # 测试查询金融产品
    test_query_financial_products()
    
    # 测试列出资源
    test_list_resources()
    
    print("测试完成!")