#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP服务器实现，提供财富管理相关查询接口
使用streamablehttp方式暴露服务
"""

from flask import Flask, request, jsonify, Response
import json
from mcp import Server
from mcp.types import Tool, Resource, Prompt
from controllers.wealth_controller import (
    query_financial_products,
    analyze_portfolio,
    assess_risk,
    predict_returns
)

# 创建Flask应用
app = Flask(__name__)

# 初始化MCP服务器，使用streamablehttp方式
mcp_server = Server(name="wealth-query-service", streamable=True)

# 注册工具函数
@mcp_server.list_tools()
def list_tools():
    return [
        Tool(
            name="query_financial_products",
            description="查询可投资的金融产品",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_type": {
                        "type": "string",
                        "description": "产品类型（基金、股票、债券等）"
                    },
                    "risk_level": {
                        "type": "string",
                        "description": "风险等级（低、中、高）"
                    }
                }
            }
        ),
        Tool(
            name="analyze_portfolio",
            description="分析投资组合表现",
            inputSchema={
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "投资组合ID"
                    }
                },
                "required": ["portfolio_id"]
            }
        ),
        Tool(
            name="assess_risk",
            description="评估投资风险",
            inputSchema={
                "type": "object",
                "properties": {
                    "investment_amount": {
                        "type": "number",
                        "description": "投资金额"
                    },
                    "investment_term": {
                        "type": "integer",
                        "description": "投资期限（月）"
                    }
                },
                "required": ["investment_amount", "investment_term"]
            }
        ),
        Tool(
            name="predict_returns",
            description="预测投资收益",
            inputSchema={
                "type": "object",
                "properties": {
                    "principal": {
                        "type": "number",
                        "description": "本金金额"
                    },
                    "annual_rate": {
                        "type": "number",
                        "description": "年化收益率"
                    },
                    "term_months": {
                        "type": "integer",
                        "description": "投资期限（月）"
                    }
                },
                "required": ["principal", "annual_rate", "term_months"]
            }
        )
    ]

# 注册工具处理函数
@mcp_server.call_tool("query_financial_products")
def handle_query_financial_products(arguments):
    return query_financial_products(
        product_type=arguments.get("product_type"),
        risk_level=arguments.get("risk_level")
    )

@mcp_server.call_tool("analyze_portfolio")
def handle_analyze_portfolio(arguments):
    return analyze_portfolio(arguments.get("portfolio_id"))

@mcp_server.call_tool("assess_risk")
def handle_assess_risk(arguments):
    return assess_risk(
        investment_amount=arguments.get("investment_amount"),
        investment_term=arguments.get("investment_term")
    )

@mcp_server.call_tool("predict_returns")
def handle_predict_returns(arguments):
    return predict_returns(
        principal=arguments.get("principal"),
        annual_rate=arguments.get("annual_rate"),
        term_months=arguments.get("term_months")
    )

# 注册资源
@mcp_server.list_resources()
def list_resources():
    return [
        Resource(
            uri="db://wealth/products",
            name="金融产品数据库",
            description="包含所有可投资金融产品的信息",
            mimeType="application/json"
        ),
        Resource(
            uri="db://wealth/portfolios/{portfolio_id}",
            name="投资组合数据",
            description="特定投资组合的详细信息",
            mimeType="application/json"
        )
    ]

# 注册资源读取函数
@mcp_server.read_resource("db://wealth/products")
def read_products():
    """读取金融产品数据"""
    return {
        "products": [
            {"id": "fund_001", "name": "稳健增长基金", "type": "基金", "risk_level": "低"},
            {"id": "stock_001", "name": "科技创新股票", "type": "股票", "risk_level": "高"},
            {"id": "bond_001", "name": "国债", "type": "债券", "risk_level": "低"}
        ]
    }

@mcp_server.read_resource("db://wealth/portfolios/{portfolio_id}")
def read_portfolio(portfolio_id: str):
    """读取特定投资组合数据"""
    # 这里应该从数据库获取实际数据
    return {
        "portfolio_id": portfolio_id,
        "total_value": 1000000,
        "assets": [
            {"product_id": "fund_001", "allocation": 0.6},
            {"product_id": "stock_001", "allocation": 0.3},
            {"product_id": "bond_001", "allocation": 0.1}
        ]
    }

# 注册提示词
@mcp_server.list_prompts()
def list_prompts():
    return [
        Prompt(
            name="wealth_advice",
            description="根据用户情况提供财富管理建议",
            arguments=[
                {"name": "age", "description": "用户年龄", "required": True},
                {"name": "income", "description": "年收入", "required": True},
                {"name": "goals", "description": "财务目标", "required": False}
            ]
        )
    ]

# 注册提示词执行函数
@mcp_server.get_prompt("wealth_advice")
def wealth_advice(age: int, income: float, goals: str = None):
    """提供财富管理建议"""
    advice = f"根据您的年龄({age}岁)和年收入({income}元)，我们建议您采取稳健的投资策略。"
    if goals:
        advice += f"针对您的财务目标'{goals}'，我们推荐适当的资产配置方案。"
    return advice

# 将MCP服务器挂载到Flask应用，支持streamablehttp
@app.route("/mcp", methods=["GET", "POST"])
def handle_mcp_request():
    return mcp_server.handle_http_request(request)

# 添加健康检查端点
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "wealth-query-service"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)