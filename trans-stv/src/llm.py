from abc import ABC, abstractmethod
import json
import re
import requests
import logging
from typing import Generator, Tuple, Any, Optional
# from langchain_experimental.llms.ollama_functions import OllamaFunctions

logger = logging.getLogger(__name__)

class LLM(ABC):
    @abstractmethod
    def response(self, dialogue) -> Generator[str, Any, None]:
        pass
        
    @abstractmethod  
    def response_call(self, dialogue, functions_call) -> Generator[Tuple[str, Optional[Any]], Any, None]:
        pass

class OllamaLLM(LLM):
    def __init__(self, config):
        # 从配置中获取参数
        self.model_name = config.get("model_name")
        self.url = config.get("url")  # 默认 URL

    def response(self, dialogue):
        try:
            # 构造请求 URL
            url = f"{self.url}/api/chat"
            data = {
                "model": self.model_name,
                "messages": dialogue,
                "stream": False
            }

            # 记录请求信息
            logger.info(f"LLM请求 - 模型: {self.model_name}, 消息数量: {len(dialogue)}, URL: {url}")
            logger.debug(f"LLM请求详情 - 数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            # 发送请求
            response = requests.post(url, json=data, stream=False)
            response.raise_for_status()  # 检查请求是否成功
            
            # 记录响应状态
            logger.info(f"LLM响应 - 状态码: {response.status_code}, 响应大小: {len(response.content)} bytes")

            # 返回响应内容
            for chunk in response.iter_lines():
                if chunk:
                    chunk_data = chunk.decode("utf-8")
                    # 解析 JSON 数据
                    parsed_data = json.loads(chunk_data)

                    # 提取 parsed_data["message"]["content"] 值
                    # print(parsed_data["message"]["content"])

                    # 使用正则表达式过滤掉<think>和</think>之间的内容
                    filtered_text = re.sub(r'<think>.*?</think>', '', parsed_data["message"]["content"], flags=re.DOTALL)

                    # 去除多余的换行符
                    filtered_text = filtered_text.strip()

                    # 定义需要替换的特殊字符
                    special_chars = {
                        "*": "",  # 替换为空格
                        "《": "",  # 删除
                        "》": "",  # 删除
                        "～": "~",  # 替换为普通波浪号
                    }

                    # 逐个替换特殊字符
                    for char, replacement in special_chars.items():
                        filtered_text = filtered_text.replace(char, replacement)
                    # print(filtered_text)

                    yield filtered_text
        except Exception as e:
            logger.error(f"Error in response generation: {e}")

    def response_call(self, dialogue, functions_call):
        try:
            # 构造请求 URL
            url = f"{self.url}/api/chat"
            data = {
                "model": self.model_name,
                "messages": dialogue,
                "stream": False
            }

            # 记录请求信息 (包含工具调用)
            tool_count = len(functions_call) if functions_call else 0
            logger.info(f"LLM工具调用请求 - 模型: {self.model_name}, 消息数量: {len(dialogue)}, 工具数量: {tool_count} (通过文本格式), URL: {url}")
            logger.debug(f"LLM工具调用请求详情 - 数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            # 发送请求
            response = requests.post(url, json=data, stream=False)
            response.raise_for_status()  # 检查请求是否成功

            # 解析响应内容（非流式响应，直接解析JSON）
            response_data = response.json()
            
            # 记录响应状态
            logger.info(f"LLM工具调用响应 - 状态码: {response.status_code}, 响应大小: {len(response.content)} bytes")
            logger.debug(f"LLM工具调用响应详情 - 数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
            
            # 检查响应格式
            if "message" not in response_data:
                logger.error(f"Invalid response format: {response_data}")
                return
                
            message = response_data["message"]
            content = message.get("content", "")
            tool_calls = message.get("tool_calls", None)
            
            # 记录关键信息
            has_tool_calls = tool_calls is not None
            content_length = len(content) if content else 0
            logger.info(f"LLM响应解析 - 内容长度: {content_length}, 是否工具调用: {has_tool_calls}")

            # 使用正则表达式过滤掉<think>和</think>之间的内容
            filtered_text = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)

            # 去除多余的换行符
            filtered_text = filtered_text.strip()
            
            # 定义需要替换的特殊字符
            special_chars = {
                "*": "",  # 替换为空格
                "《": "",  # 删除
                "》": "",  # 删除
                "～": "~",  # 替换为普通波浪号
            }

            # 逐个替换特殊字符
            for char, replacement in special_chars.items():
                filtered_text = filtered_text.replace(char, replacement)
                
            # 返回处理后的内容和工具调用信息
            yield filtered_text, tool_calls
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error in response_call: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in response_call: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in response_call: {e}")

    def response_call_stream(self, dialogue, functions_call):
        """
        支持流式工具调用：
        tools: list of tool definitions, e.g. [{"type":"function","function":{...}}, ...]
        """
        try:

            url = f"{self.url}/api/chat"
            data = {
                "model": self.model_name,
                "messages": dialogue,
                "stream": True
            }
        
    
            # 记录请求信息 (包含工具调用)
            tool_count = len(functions_call) if functions_call else 0
            logger.info(f"LLM工具调用请求 - 模型: {self.model_name}, 消息数量: {len(dialogue)}, 工具数量: {tool_count}, URL: {url}")
            logger.debug(f"LLM工具调用请求详情 - 数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            # 发送请求
            response = requests.post(url, json=data, stream=True)
            response.raise_for_status()  # 检查请求是否成功   

            # 记录响应状态
            logger.info(f"LLM工具调用响应 - 状态码: {response.status_code}, Content-Type: {response.headers.get('content-type', 'unknown')}")

            chunk_count = 0
            for line in response.iter_lines():
                if not line:
                    continue
                chunk_count += 1
                data = json.loads(line.decode())
                msg = data.get("message", {})
                content = msg.get("content")
                tool_calls = msg.get("tool_calls")
                
                # 区分文本响应与工具调用的日志格式
                if tool_calls is not None:
                    logger.debug(f"LLM工具调用chunk {chunk_count} - 工具调用: {tool_calls}")
                elif content is not None:
                    logger.debug(f"LLM文本响应chunk {chunk_count} - 内容: '{content}'")
                
                yield content, tool_calls
                
            logger.info(f"LLM流式响应完成 - 总共{chunk_count}个chunk")
        except Exception as e:
            logger.error(f"OllamaLLM tool-call error: {e}")

def create_instance(class_name, *args, **kwargs):
    # 获取类对象
    cls = globals().get(class_name)
    if cls:
        # 创建并返回实例
        return cls(*args, **kwargs)
    else:
        raise ValueError(f"Class {class_name} not found")


if __name__ == "__main__":
    # 配置
    config = {
        "model_name": "qwen3:0.6b",
        "url": "http://localhost:11434",
        "api_key": None  # 如果没有 API Key，可以设置为 None
    }

    # 创建 OllamaLLM 的实例
    ollama = create_instance("OllamaLLM", config)
    dialogue = [{"role": "user", "content": "你是谁"}]

    # 打印逐步生成的响应内容
    for chunk in ollama.response(dialogue):
        print(chunk)

