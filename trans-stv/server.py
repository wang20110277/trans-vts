import os
# 禁止生成 __pycache__ 文件
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import time
import threading
import argparse
import json
import logging
import asyncio
import uvicorn
import socket
from fastapi import FastAPI, WebSocket, Query, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, List
from pydantic import BaseModel
import json
import logging

# 配置日志记录
# 确保temp目录存在
TEMP_DIR = "tmp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.FileHandler(os.path.join(TEMP_DIR, 'server.log'))  # 文件输出到temp目录
    ]
)

from src import robot
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Description of your script.")

# Add arguments
parser.add_argument('--config_path', type=str, help="配置文件", default="config/config.yaml")

# Parse arguments
args = parser.parse_args()
config_path = args.config_path

# 存储对话历史
dialogue: List[Dict] = []
# 存储用户对话历史
user_dialogues: Dict[str, List[Dict]] = {}
active_robots: Dict[str, list] = {}
# 存储WebRTC连接
webrtc_connections: Dict[str, WebSocket] = {}
TIMEOUT = 600

# 语音文件存储目录
AUDIO_DIR = os.path.join(TEMP_DIR, "audio")
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)
    logger.info(f"创建语音文件存储目录: {AUDIO_DIR}")

# 清理超时连接的任务
async def cleanup_task():
    while True:
        now = time.time()
        for uid, (robot_instance, ts) in list(active_robots.items()):
            if now - ts > TIMEOUT:
                try:
                    robot_instance.recorder.stop_recording()
                    robot_instance.shutdown()
                    logger.info(f"{uid} 对应的robot已释放")
                except Exception as e:
                    logger.info(f"{uid} 对应的robot释放 出错: {e}")
                active_robots.pop(uid, None)
        await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    logger.info("服务器启动")
    # 启动清理任务
    task = asyncio.create_task(cleanup_task())
    yield
    # 关闭时执行
    task.cancel()
    await task
    logger.info("服务器关闭")

app = FastAPI(lifespan=lifespan)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（必须在路由定义之前）
if os.path.exists("templates"):
    app.mount("/static", StaticFiles(directory="templates"), name="static")

# 理财产品数据模型
class FinancialProduct(BaseModel):
    id: int
    name: str
    type: str
    risk_level: str
    expected_return: float
    description: str

# 理财咨询请求模型
class FinancialAdviceRequest(BaseModel):
    question: str
    risk_tolerance: str = "稳健型"
    investment_amount: float = 10000

# 理财产品推荐请求模型
class ProductRecommendationRequest(BaseModel):
    risk_tolerance: str
    investment_term: str
    amount: float

# 挂载assets目录以提供图片等静态资源
assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# 模拟理财产品数据
financial_products = [
    FinancialProduct(id=1, name="稳健增长混合基金", type="基金", risk_level="稳健型", expected_return=5.2, description="主要投资于优质股票和债券，风险适中，收益稳定"),
    FinancialProduct(id=2, name="科技创新股票基金", type="基金", risk_level="积极型", expected_return=8.5, description="专注于科技创新领域的优质上市公司股票"),
    FinancialProduct(id=3, name="国债逆回购", type="债券", risk_level="保守型", expected_return=2.8, description="安全性极高，流动性好的短期投资工具"),
    FinancialProduct(id=4, name="货币市场基金", type="基金", risk_level="保守型", expected_return=3.0, description="投资于短期货币工具，流动性极佳"),
    FinancialProduct(id=5, name="黄金ETF", type="商品", risk_level="稳健型", expected_return=4.5, description="跟踪黄金价格变动，对抗通胀的良好工具"),
]

@app.get("/api/products")
async def get_financial_products():
    """获取所有理财产品列表"""
    return financial_products

@app.get("/api/products/{product_id}")
async def get_financial_product(product_id: int):
    """根据ID获取特定理财产品信息"""
    for product in financial_products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="理财产品未找到")

@app.post("/api/advice")
async def get_financial_advice(request: FinancialAdviceRequest):
    """获取理财建议"""
    # 这里应该调用实际的理财咨询逻辑
    advice = f"关于您的问题'{request.question}'，结合您的风险偏好{request.risk_tolerance}和投资金额{request.investment_amount}元，我为您提供以下建议：\n\n"
    
    if "投资组合" in request.question:
        advice += "1. 建议采用分散投资策略，不要把所有资金投入单一资产。\n"
        advice += "2. 根据您的风险承受能力，可以考虑股票、债券、基金等多元化配置。\n"
        advice += "3. 定期调整投资组合，以适应市场变化和个人目标的变化。"
    elif "低风险" in request.question:
        advice += "1. 推荐考虑国债、银行定期存款等固定收益类产品。\n"
        advice += "2. 货币基金和债券基金也是不错的选择。\n"
        advice += "3. 避免高波动性的投资产品。"
    else:
        advice += "1. 建议您首先明确自己的投资目标和风险承受能力。\n"
        advice += "2. 制定合理的资产配置计划。\n"
        advice += "3. 定期评估和调整您的投资策略。"
    
    return {"advice": advice}

@app.post("/api/recommendations")
async def get_product_recommendations(request: ProductRecommendationRequest):
    """根据用户需求推荐理财产品"""
    # 这里应该调用实际的产品推荐逻辑
    recommendations = []
    
    if request.risk_tolerance == "保守型":
        recommendations = [p for p in financial_products if p.risk_level == "保守型"]
    elif request.risk_tolerance == "稳健型":
        recommendations = [p for p in financial_products if p.risk_level in ["保守型", "稳健型"]]
    elif request.risk_tolerance == "积极型":
        recommendations = [p for p in financial_products if p.risk_level in ["稳健型", "积极型"]]
    else:
        recommendations = financial_products
    
    return {"recommendations": recommendations}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Query(...)):
    """处理WebSocket连接"""
    await websocket.accept()
    loop = asyncio.get_event_loop()
    logger.info("WebSocket连接已建立")
    if user_id not in active_robots:
        active_robots[user_id] = [robot.Robot(config_path, websocket, loop), time.time()]
        threading.Thread(target=active_robots[user_id][0].run, daemon=True).start()
    robot_instance = active_robots[user_id][0]
    logger.info(f"用户 {user_id} 已连接")
    
    try:
        while True:
            msg = await websocket.receive()

            if "bytes" in msg:
                robot_instance.recorder.put_audio(msg["bytes"])
            elif "text" in msg:
                logger.info(f"收到请求:{msg}")
                message_data = json.loads(msg["text"])
                logger.info(f"收到请求:{message_data.get('content', '')}")
                content = message_data.get("content", "")
                # 处理用户消息
                response_message=robot_instance.chat_tool_tts(content)
                
                # 通过WebSocket将response_message返回给前端
                if response_message is not None:
                    # 发送完整的对话历史，而不仅仅是当前的用户消息和助手回复
                    full_dialogue = robot_instance.dialogue.get_llm_dialogue()
                    await websocket.send_text(json.dumps({
                        "type": "update_dialogue",
                        "data": full_dialogue
                    }, ensure_ascii=False))
                logger.info(f"返回结果: {response_message}")
            active_robots[user_id][1] = time.time()

    except WebSocketDisconnect:
        logger.info(f"用户 {user_id} 断开连接")
    except Exception as e:
        logger.error(f"处理WebSocket消息时出错: {e}")
    finally:
        logger.info("WebSocket连接已关闭")


@app.websocket("/webrtc")
async def webrtc_endpoint(websocket: WebSocket, user_id: str = Query(...)):
    """处理WebRTC信令服务器连接"""
    await websocket.accept()
    logger.info(f"WebRTC连接已建立，用户ID: {user_id}")
    
    # 存储连接
    webrtc_connections[user_id] = websocket
    
    try:
        while True:
            # 接收信令消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.info(f"收到WebRTC信令消息: {message['type']}")
            
            # 处理不同类型的信令消息
            if message['type'] == 'offer' or message['type'] == 'answer' or message['type'] == 'ice-candidate':
                # 转发消息给其他用户（在实际应用中可能需要更复杂的逻辑）
                # 这里简化处理，假设只有两个用户在通话
                for uid, ws in webrtc_connections.items():
                    if uid != user_id and ws.client_state.CONNECTED:
                        await ws.send_text(data)
                        break
            
    except WebSocketDisconnect:
        logger.info(f"用户 {user_id} WebRTC连接断开")
    except Exception as e:
        logger.error(f"处理WebRTC消息时出错: {e}")
    finally:
        # 清理连接
        if user_id in webrtc_connections:
            del webrtc_connections[user_id]
        logger.info("WebRTC连接已关闭")

def get_lan_ip():
    try:
        # 创建一个UDP套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到Google DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return "无法获取IP: " + str(e)

if __name__ == '__main__':
    lan_ip = get_lan_ip()
    print(f"\n请在局域网中使用以下地址访问:")
    print(f"https://{lan_ip}:8000\n")
    logger.info("阿雅语音助手已启动")
    logger.info("支持语音输入和文本输入，可以转为语音回复")
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # 生产环境中关闭自动重载
        log_level="info"
    )