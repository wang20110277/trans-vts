#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用FastMCP重构的MCP服务器实现，提供财富管理相关查询接口
"""

from fastmcp import FastMCP
from controllers.wealth_controller import (
    query_financial_products,
    analyze_portfolio,
    assess_risk,
    predict_returns
)

# 初始化FastMCP服务器
mcp = FastMCP(name="wealth-query-service")

# 注册工具函数
@mcp.tool(
    name="query_financial_products",
    description="查询可投资的金融产品"
)
def tool_query_financial_products(product_type: str = None, risk_level: str = None):
    """查询可投资的金融产品"""
    return query_financial_products(product_type=product_type, risk_level=risk_level)


@mcp.tool(
    name="analyze_portfolio",
    description="分析投资组合表现"
)
def tool_analyze_portfolio(portfolio_id: str):
    """分析投资组合表现"""
    return analyze_portfolio(portfolio_id)


@mcp.tool(
    name="assess_risk",
    description="评估投资风险"
)
def tool_assess_risk(investment_amount: float, investment_term: int):
    """评估投资风险"""
    return assess_risk(investment_amount=investment_amount, investment_term=investment_term)


@mcp.tool(
    name="predict_returns",
    description="预测投资收益"
)
def tool_predict_returns(principal: float, annual_rate: float, term_months: int):
    """预测投资收益"""
    return predict_returns(principal=principal, annual_rate=annual_rate, term_months=term_months)


# 注册资源
@mcp.resource(
    uri="db://wealth/products",
    name="金融产品数据库",
    description="包含所有可投资金融产品的信息",
    mime_type="application/json"
)
def resource_products():
    """读取金融产品数据"""
    return {
        "products": [
            {"id": "fund_001", "name": "稳健增长基金", "type": "基金", "risk_level": "低"},
            {"id": "stock_001", "name": "科技创新股票", "type": "股票", "risk_level": "高"},
            {"id": "bond_001", "name": "国债", "type": "债券", "risk_level": "低"}
        ]
    }


@mcp.resource(
    uri="db://wealth/portfolios/{portfolio_id}",
    name="投资组合数据",
    description="特定投资组合的详细信息",
    mime_type="application/json"
)
def resource_portfolio(portfolio_id: str):
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
@mcp.prompt(
    name="wealth_advice",
    description="根据用户情况提供财富管理建议"
)
def prompt_wealth_advice(age: int, income: float, goals: str = None):
    """提供财富管理建议"""
    advice = f"根据您的年龄({age}岁)和年收入({income}元)，我们建议您采取稳健的投资策略。"
    if goals:
        advice += f"针对您的财务目标'{goals}'，我们推荐适当的资产配置方案。"
    return advice


if __name__ == "__main__":
    # 运行FastMCP服务器
    mcp.run(host="0.0.0.0", port=8000, debug=True)