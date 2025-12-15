#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用FastMCP客户端测试财富查询服务的脚本
"""

import asyncio
from fastmcp import Client

async def test_client():
    """测试FastMCP客户端连接"""
    # 创建客户端连接到本地服务
    async with Client("http://localhost:8000/mcp") as client:
        print("Connected to FastMCP server")
        
        # 列出所有工具
        print("\nListing tools...")
        tools = await client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # 测试查询金融产品工具
        print("\nTesting query_financial_products...")
        result = await client.call_tool(
            "query_financial_products",
            {"risk_level": "低"}
        )
        print(f"Low risk products: {result}")
        
        # 测试分析投资组合工具
        print("\nTesting analyze_portfolio...")
        result = await client.call_tool(
            "analyze_portfolio",
            {"portfolio_id": "portfolio_001"}
        )
        print(f"Portfolio analysis: {result}")

if __name__ == "__main__":
    print("Testing FastMCP Wealth Query Service with Client\n")
    
    # 启动异步测试
    asyncio.run(test_client())
    
    print("\n测试完成!")