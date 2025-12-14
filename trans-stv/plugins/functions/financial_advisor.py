import logging
from plugins.registry import register_function, ActionResponse, Action

logger = logging.getLogger(__name__)

@register_function('financial_advisor')
def financial_advisor(query: str):
    """
    提供专业的理财咨询服务
    
    Args:
        query (str): 用户的理财相关问题
        
    Returns:
        ActionResponse: 包含理财建议的响应
    """
    # 这里应该是调用实际的理财咨询逻辑
    # 目前我们返回一个模拟的响应
    
    advice = f"关于您的问题'{query}'，我为您提供以下理财建议：\n\n"
    
    if "投资组合" in query or "资产配置" in query:
        advice += "1. 建议采用分散投资策略，不要把所有资金投入单一资产。\n"
        advice += "2. 根据您的风险承受能力，可以考虑股票、债券、基金等多元化配置。\n"
        advice += "3. 定期调整投资组合，以适应市场变化和个人目标的变化。"
    elif "低风险" in query:
        advice += "1. 推荐考虑国债、银行定期存款等固定收益类产品。\n"
        advice += "2. 货币基金和债券基金也是不错的选择。\n"
        advice += "3. 避免高波动性的投资产品。"
    elif "基金" in query:
        advice += "1. 根据投资期限选择合适的基金类型。\n"
        advice += "2. 关注基金的历史业绩和基金经理的投资能力。\n"
        advice += "3. 定投是一种降低风险的有效策略。"
    else:
        advice += "1. 建议您首先明确自己的投资目标和风险承受能力。\n"
        advice += "2. 制定合理的资产配置计划。\n"
        advice += "3. 定期评估和调整您的投资策略。"
    
    return ActionResponse(Action.RESPONSE, None, advice)


@register_function('product_recommendation')
def product_recommendation(risk_tolerance: str, investment_term: str, amount: float):
    """
    根据用户需求推荐理财产品
    
    Args:
        risk_tolerance (str): 风险承受能力
        investment_term (str): 投资期限
        amount (float): 投资金额
        
    Returns:
        ActionResponse: 包含产品推荐的响应
    """
    # 这里应该是调用实际的产品推荐逻辑
    # 目前我们返回一个模拟的响应
    
    recommendation = f"根据您的风险偏好{risk_tolerance}、投资期限{investment_term}和投资金额{amount}元，我为您推荐以下理财产品：\n\n"
    
    if risk_tolerance == "保守型":
        recommendation += "1. 银行定期存款：安全性高，收益稳定。\n"
        recommendation += "2. 国债：国家信用担保，风险极低。\n"
        recommendation += "3. 货币基金：流动性好，收益略高于活期存款。"
    elif risk_tolerance == "稳健型":
        recommendation += "1. 债券基金：收益相对稳定，风险适中。\n"
        recommendation += "2. 混合型基金：股债配置，平衡风险与收益。\n"
        recommendation += "3. 银行理财产品：专业管理，多样化投资。"
    elif risk_tolerance == "积极型":
        recommendation += "1. 股票型基金：追求较高收益，适合中长期投资。\n"
        recommendation += "2. 指数基金：跟踪市场指数，费用较低。\n"
        recommendation += "3. 行业主题基金：聚焦特定行业，把握行业增长机会。"
    elif risk_tolerance == "激进型":
        recommendation += "1. 成长型股票基金：投资高成长性公司，潜在收益高。\n"
        recommendation += "2. 科技行业基金：投资前沿科技领域，高风险高收益。\n"
        recommendation += "3. QDII基金：全球资产配置，分散地域风险。"
    else:
        recommendation += "1. 建议您重新评估风险承受能力。\n"
        recommendation += "2. 可以考虑咨询专业的理财顾问。\n"
        recommendation += "3. 从低风险产品开始，逐步了解各类投资产品。"
    
    return ActionResponse(Action.RESPONSE, None, recommendation)


if __name__ == "__main__":
    # 测试函数
    result = financial_advisor("如何配置我的投资组合？")
    print(result.response)
    
    result = product_recommendation("稳健型", "中期", 100000)
    print(result.response)