from abc import ABC, abstractmethod
import openai
import logging


logger = logging.getLogger(__name__)


class LLM(ABC):
    @abstractmethod
    def response(self, dialogue):
        pass


class OpenAILLM(LLM):
    def __init__(self, config):
        self.model_name = config.get("model_name")
        self.api_key = config.get("api_key")
        self.base_url = config.get("url")
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def response(self, dialogue):
        try:
            # 记录请求信息
            logger.info(f"LLM请求 - 模型: {self.model_name}, 消息数量: {len(dialogue)}, 基础URL: {self.base_url}")
            logger.debug(f"LLM请求详情 - 对话: {dialogue}")
            
            responses = self.client.chat.completions.create(  #) ChatCompletion.create(
                model=self.model_name,
                messages=dialogue,
                stream=True
            )
            
            logger.info(f"LLM流式响应开始 - 模型: {self.model_name}")
            
            chunk_count = 0
            for chunk in responses:
                chunk_count += 1
                content = chunk.choices[0].delta.content
                logger.debug(f"LLM流式chunk {chunk_count} - 内容: '{content}'")
                yield content
                
            logger.info(f"LLM流式响应完成 - 总共{chunk_count}个chunk")
        except Exception as e:
            logger.error(f"Error in response generation: {e}")

    def response_call(self, dialogue, functions_call):
        try:
            # 记录请求信息 (包含工具调用)
            tool_count = len(functions_call) if functions_call else 0
            logger.info(f"LLM工具调用请求 - 模型: {self.model_name}, 消息数量: {len(dialogue)}, 工具数量: {tool_count}")
            logger.debug(f"LLM工具调用请求详情 - 对话: {dialogue}, 工具: {functions_call}")
            
            responses = self.client.chat.completions.create(  #) ChatCompletion.create(
                model=self.model_name,
                messages=dialogue,
                stream=True,
                tools=functions_call
            )
            
            logger.info(f"LLM工具调用流式响应开始 - 模型: {self.model_name}")
            
            chunk_count = 0
            for chunk in responses:
                chunk_count += 1
                content = chunk.choices[0].delta.content
                tool_calls = chunk.choices[0].delta.tool_calls
                
                # 区分文本响应与工具调用的日志格式
                if tool_calls is not None:
                    logger.debug(f"LLM工具调用chunk {chunk_count} - 工具调用: {tool_calls}")
                elif content is not None:
                    logger.debug(f"LLM文本响应chunk {chunk_count} - 内容: '{content}'")
                
                yield content, tool_calls
                
            logger.info(f"LLM工具调用流式响应完成 - 总共{chunk_count}个chunk")
        except Exception as e:
            logger.error(f"Error in response generation: {e}")


def create_instance(class_name, *args, **kwargs):
    # 获取类对象
    cls = globals().get(class_name)
    if cls:
        # 创建并返回实例
        return cls(*args, **kwargs)
    else:
        raise ValueError(f"Class {class_name} not found")


if __name__ == "__main__":
    # 创建 DeepSeekLLM 的实例
    deepseek = create_instance("DeepSeekLLM", api_key="your_api_key", base_url="your_base_url")
    dialogue = [{"role": "user", "content": "hello"}]

    # 打印逐步生成的响应内容
    for chunk in deepseek.response(dialogue):
        print(chunk)
