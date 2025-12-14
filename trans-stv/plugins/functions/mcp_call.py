import json
import subprocess
import logging
import os
import time
import asyncio
from typing import Optional, Dict, Any, AsyncGenerator, Union
from plugins.registry import register_function, ToolType, Action, ActionResponse

logger = logging.getLogger(__name__)

# MCP配置文件路径，可以通过环境变量覆盖
MCP_CONFIG_PATH = os.environ.get("MCP_CONFIG_PATH", "mcp_config.json")

# 注册MCP调用函数
@register_function("mcp_call", ToolType.WAIT)
def mcp_call(
    server_name: str,
    command: Optional[str] = None,
    args: Optional[list] = None,
    timeout: int = 30,
    check_status: bool = True
) -> ActionResponse:
    """
    调用MCP服务器执行命令
    
    Args:
        server_name (str): MCP服务器名称
        command (str, optional): 要执行的命令
        args (list, optional): 命令参数列表
        timeout (int, optional): 命令执行超时时间(秒)，默认30秒
        check_status (bool, optional): 是否检查服务器状态，默认True
    
    Returns:
        ActionResponse: 包含执行结果的响应对象
    """
    try:
        # 读取MCP服务器配置
        mcp_config = _load_mcp_config()
        
        # 检查服务器是否存在
        if server_name not in mcp_config.get("mcpServers", {}):
            return ActionResponse(
                action=Action.RESPONSE,
                result=None,
                response=f"MCP服务器 '{server_name}' 未找到"
            )
        
        # 获取服务器配置
        server_config = mcp_config["mcpServers"][server_name]
        cmd = server_config["command"]
        
        # 构建命令参数
        cmd_args = server_config.get("args", [])
        if command:
            cmd_args.append(command)
        if args:
            cmd_args.extend(args)
        
        # 检查服务器状态（如果需要）
        if check_status:
            status_result = _check_server_status(server_name, server_config)
            if not status_result.success:
                return ActionResponse(
                    action=Action.RESPONSE,
                    result=None,
                    response=f"MCP服务器 '{server_name}' 状态检查失败: {status_result.message}"
                )
        
        # 执行命令
        logger.info(f"执行MCP命令: {cmd} {' '.join(cmd_args)}")
        start_time = time.time()
        result = subprocess.run(
            [cmd] + cmd_args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        execution_time = time.time() - start_time
        logger.info(f"MCP命令执行完成，耗时: {execution_time:.2f}秒")
        
        # 检查执行结果
        if result.returncode == 0:
            output = result.stdout.strip()
            logger.debug(f"MCP命令执行成功，输出: {output}")
            return ActionResponse(
                action=Action.RESPONSE,
                result=output,
                response=output
            )
        else:
            error_msg = result.stderr.strip()
            logger.error(f"MCP命令执行失败 (返回码: {result.returncode}): {error_msg}")
            return ActionResponse(
                action=Action.RESPONSE,
                result=None,
                response=f"执行MCP命令时出错 (返回码: {result.returncode}): {error_msg}"
            )
            
    except subprocess.TimeoutExpired:
        logger.error(f"MCP命令执行超时 (>{timeout}秒)")
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"MCP命令执行超时 (>{timeout}秒)"
        )
    except FileNotFoundError as e:
        logger.error(f"未找到MCP命令: {str(e)}")
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"未找到MCP命令: {str(e)}"
        )
    except PermissionError as e:
        logger.error(f"MCP命令执行权限不足: {str(e)}")
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"MCP命令执行权限不足: {str(e)}"
        )
    except Exception as e:
        logger.error(f"MCP调用出错: {str(e)}", exc_info=True)
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"MCP调用出错: {str(e)}"
        )

class ServerStatusResult:
    """服务器状态检查结果"""
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message


def _check_server_status(server_name: str, server_config: Dict[str, Any]) -> ServerStatusResult:
    """
    检查MCP服务器状态
    
    Args:
        server_name (str): 服务器名称
        server_config (Dict[str, Any]): 服务器配置
    
    Returns:
        ServerStatusResult: 状态检查结果
    """
    try:
        # 这里实现服务器状态检查逻辑
        # 对于不同类型的服务器，可能需要不同的检查方法
        logger.info(f"检查MCP服务器 '{server_name}' 状态...")
        
        # 示例：发送一个简单的命令来检查服务器是否响应
        cmd = server_config["command"]
        cmd_args = server_config.get("status_args", ["--status"])
        
        result = subprocess.run(
            [cmd] + cmd_args,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            logger.info(f"MCP服务器 '{server_name}' 状态正常")
            return ServerStatusResult(True, "服务器状态正常")
        else:
            error_msg = result.stderr.strip() or "未知错误"
            logger.warning(f"MCP服务器 '{server_name}' 状态异常: {error_msg}")
            return ServerStatusResult(False, error_msg)
    
    except Exception as e:
        logger.error(f"检查MCP服务器 '{server_name}' 状态时出错: {str(e)}")
        return ServerStatusResult(False, str(e))

def _load_mcp_config() -> Dict[str, Any]:
    """
    加载MCP配置
    
    Returns:
        dict: MCP配置字典
    """
    # 默认配置
    default_config = {
        "mcpServers": {}
    }
    
    # 尝试从文件加载配置
    config_path = MCP_CONFIG_PATH
    try:
        logger.info(f"加载MCP配置文件: {config_path}")
        
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        # 验证配置格式
        if not isinstance(config, dict) or "mcpServers" not in config:
            logger.warning("MCP配置格式不正确，使用默认配置")
            return default_config
        
        return config
    except FileNotFoundError:
        logger.warning(f"未找到MCP配置文件: {config_path}，使用默认配置")
        return default_config
    except json.JSONDecodeError as e:
        logger.error(f"解析MCP配置文件出错: {str(e)}")
        return default_config
    except Exception as e:
        logger.error(f"加载MCP配置时出错: {str(e)}")
        return default_config

# 异步版本的MCP调用（支持stdio和SSE调用）
@register_function("mcp_call_async", ToolType.TIME_CONSUMING)
async def mcp_call_async(
    server_name: str,
    command: Optional[str] = None,
    args: Optional[list] = None,
    timeout: int = 30,
    sse_mode: bool = False,
    task_id: Optional[str] = None
) -> Union[ActionResponse, AsyncGenerator[str, None]]:
    """
    异步调用MCP服务器执行命令（支持stdio和SSE流式调用）
    
    Args:
        server_name (str): MCP服务器名称
        command (str, optional): 要执行的命令
        args (list, optional): 命令参数列表
        timeout (int, optional): 命令执行超时时间(秒)，默认30秒
        sse_mode (bool, optional): 是否启用SSE流式模式，默认False
        task_id (str, optional): 任务ID，SSE模式下使用
    
    Returns:
        Union[ActionResponse, AsyncGenerator[str, None]]: 
            stdio模式返回ActionResponse，SSE模式返回异步生成器
    """
    try:
        # 读取MCP服务器配置
        mcp_config = _load_mcp_config()
        
        # 检查服务器是否存在
        if server_name not in mcp_config.get("mcpServers", {}):
            error_response = ActionResponse(
                action=Action.RESPONSE,
                result=None,
                response=f"MCP服务器 '{server_name}' 未找到"
            )
            if sse_mode:
                if task_id is None:
                    task_id = f"mcp_error_{int(time.time() * 1000)}"
                return _generate_error_sse_stream(task_id, f"MCP服务器 '{server_name}' 未找到")
            return error_response
        
        # 获取服务器配置
        server_config = mcp_config["mcpServers"][server_name]
        cmd = server_config["command"]
        
        # 构建命令参数
        cmd_args = server_config.get("args", [])
        if command:
            cmd_args.append(command)
        if args:
            cmd_args.extend(args)
        
        # 根据调用模式选择执行方式
        if sse_mode:
            if task_id is None:
                task_id = f"mcp_{server_name}_{int(time.time() * 1000)}"
            return _execute_mcp_with_sse_stream(cmd, cmd_args, timeout, task_id, server_name, command or "default")
        else:
            return await _execute_mcp_stdio(cmd, cmd_args, timeout)

    except FileNotFoundError as e:
        error_msg = f"未找到异步MCP命令: {str(e)}"
        logger.error(error_msg)
        if sse_mode:
            if task_id is None:
                task_id = f"mcp_error_{int(time.time() * 1000)}"
            return _generate_error_sse_stream(task_id, error_msg)
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=error_msg
        )
    except Exception as e:
        error_msg = f"异步MCP调用出错: {str(e)}"
        logger.error(error_msg, exc_info=True)
        if sse_mode:
            if task_id is None:
                task_id = f"mcp_error_{int(time.time() * 1000)}"
            return _generate_error_sse_stream(task_id, error_msg)
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=error_msg
        )

# 查询异步MCP任务结果
@register_function("mcp_get_result", ToolType.WAIT)
def mcp_get_result(task_id: str) -> ActionResponse:
    """
    查询异步MCP任务结果
    
    Args:
        task_id (str): 任务ID
    
    Returns:
        ActionResponse: 包含任务结果的响应对象
    """
    try:
        from plugins.task_manager import TaskManager
        
        if not TaskManager.task_exists(task_id):
            return ActionResponse(
                action=Action.RESPONSE,
                result=None,
                response=f"任务ID '{task_id}' 不存在"
            )
        
        if not TaskManager.task_completed(task_id):
            return ActionResponse(
                action=Action.RESPONSE,
                result={"status": "running"},
                response=f"任务 '{task_id}' 仍在执行中"
            )
        
        result = TaskManager.get_task_result(task_id)
        
        if isinstance(result, ActionResponse):
            return result
        else:
            return ActionResponse(
                action=Action.RESPONSE,
                result=result,
                response=f"任务 '{task_id}' 执行结果: {result}"
            )
    except Exception as e:
        logger.error(f"查询MCP任务结果时出错: {str(e)}")
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"查询MCP任务结果时出错: {str(e)}"
        )


# ==== 新增的辅助函数：支持stdio和SSE两种调用模式 ====

async def _execute_mcp_stdio(cmd: str, cmd_args: list, timeout: int) -> ActionResponse:
    """
    执行MCP命令（stdio模式）
    
    Args:
        cmd (str): 命令名称
        cmd_args (list): 命令参数
        timeout (int): 超时时间
    
    Returns:
        ActionResponse: 执行结果
    """
    logger.info(f"执行stdio模式MCP命令: {cmd} {' '.join(cmd_args)}")
    start_time = time.time()
    
    try:
        # 使用 asyncio 的 subprocess 进行异步执行
        process = await asyncio.create_subprocess_exec(
            cmd, *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
            
            execution_time = time.time() - start_time
            logger.info(f"stdio模式MCP命令执行完成，耗时: {execution_time:.2f}秒")
            
            # 检查执行结果
            if process.returncode == 0:
                output = stdout.decode('utf-8').strip()
                logger.debug(f"stdio模式MCP命令执行成功，输出: {output}")
                return ActionResponse(
                    action=Action.RESPONSE,
                    result=output,
                    response=output
                )
            else:
                error_msg = stderr.decode('utf-8').strip()
                logger.error(f"stdio模式MCP命令执行失败 (返回码: {process.returncode}): {error_msg}")
                return ActionResponse(
                    action=Action.RESPONSE,
                    result=None,
                    response=f"执行stdio模式MCP命令时出错 (返回码: {process.returncode}): {error_msg}"
                )
                
        except asyncio.TimeoutError:
            # 终止进程
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                process.kill()
                
            logger.error(f"stdio模式MCP命令执行超时 (>{timeout}秒)")
            return ActionResponse(
                action=Action.RESPONSE,
                result=None,
                response=f"stdio模式MCP命令执行超时 (>{timeout}秒)"
            )
            
    except Exception as e:
        logger.error(f"stdio模式MCP执行出错: {str(e)}", exc_info=True)
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"stdio模式MCP执行出错: {str(e)}"
        )


async def _execute_mcp_with_sse_stream(
    cmd: str, 
    cmd_args: list, 
    timeout: int, 
    task_id: str, 
    server_name: str, 
    command: str
) -> AsyncGenerator[str, None]:
    """
    执行MCP命令（SSE流式模式）
    
    Args:
        cmd (str): 命令名称
        cmd_args (list): 命令参数
        timeout (int): 超时时间
        task_id (str): 任务ID
        server_name (str): 服务器名称
        command (str): 执行的命令
    
    Yields:
        str: SSE事件数据
    """
    try:
        # 发送开始事件
        yield f"data: {{\"type\": \"start\", \"task_id\": \"{task_id}\", \"message\": \"开始调用 {server_name} MCP 服务器\"}}\n\n"
        
        logger.info(f"执行SSE模式MCP命令: {cmd} {' '.join(cmd_args)}")
        
        # 发送进度事件
        yield f"data: {{\"type\": \"progress\", \"task_id\": \"{task_id}\", \"message\": \"正在执行命令: {command or 'default'}\"}}\n\n"
        
        start_time = time.time()
        
        # 创建异步子进程
        process = await asyncio.create_subprocess_exec(
            cmd, *cmd_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            # 等待进程完成或超时
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
            
            execution_time = time.time() - start_time
            logger.info(f"SSE模式MCP命令执行完成，耗时: {execution_time:.2f}秒")
            
            # 检查执行结果
            if process.returncode == 0:
                output = stdout.decode('utf-8').strip()
                logger.debug(f"SSE模式MCP命令执行成功，输出: {output}")
                
                # 发送成功事件
                yield f"data: {{\"type\": \"success\", \"task_id\": \"{task_id}\", \"result\": {json.dumps(output, ensure_ascii=False)}}}\n\n"
            else:
                error_msg = stderr.decode('utf-8').strip()
                logger.error(f"SSE模式MCP命令执行失败 (返回码: {process.returncode}): {error_msg}")
                
                # 发送错误事件
                yield f"data: {{\"type\": \"error\", \"task_id\": \"{task_id}\", \"message\": {json.dumps(f'执行失败 (返回码: {process.returncode}): {error_msg}', ensure_ascii=False)}}}\n\n"
                
        except asyncio.TimeoutError:
            # 终止进程
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                process.kill()
                
            logger.error(f"SSE模式MCP命令执行超时 (>{timeout}秒)")
            
            # 发送超时错误事件
            yield f"data: {{\"type\": \"error\", \"task_id\": \"{task_id}\", \"message\": \"MCP调用超时 (>{timeout}秒)\"}}\n\n"
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"SSE模式MCP执行出错: {error_msg}", exc_info=True)
        
        # 发送错误事件
        yield f"data: {{\"type\": \"error\", \"task_id\": \"{task_id}\", \"message\": {json.dumps(f'执行出错: {error_msg}', ensure_ascii=False)}}}\n\n"
    
    finally:
        # 发送结束事件
        yield f"data: {{\"type\": \"end\", \"task_id\": \"{task_id}\"}}\n\n"


async def _generate_error_sse_stream(task_id: str, error_message: str) -> AsyncGenerator[str, None]:
    """
    生成错误SSE流
    
    Args:
        task_id (str): 任务ID
        error_message (str): 错误消息
    
    Yields:
        str: SSE事件数据
    """
    yield f"data: {{\"type\": \"start\", \"task_id\": \"{task_id}\", \"message\": \"MCP调用启动\"}}\n\n"
    yield f"data: {{\"type\": \"error\", \"task_id\": \"{task_id}\", \"message\": {json.dumps(error_message, ensure_ascii=False)}}}\n\n"
    yield f"data: {{\"type\": \"end\", \"task_id\": \"{task_id}\"}}\n\n"


# ==== MCP调用的便捷函数 ====

def create_mcp_call_stdio(server_name: str, command: Optional[str] = None, args: Optional[list] = None, timeout: int = 30) -> ActionResponse:
    """
    创建stdio模式的MCP调用（同步封装）
    
    Args:
        server_name (str): MCP服务器名称
        command (str, optional): 要执行的命令
        args (list, optional): 命令参数列表
        timeout (int, optional): 超时时间
    
    Returns:
        ActionResponse: 执行结果
    """
    import asyncio
    
    try:
        # 获取或创建事件循环
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # 运行异步调用
        result = loop.run_until_complete(
            mcp_call_async(server_name, command, args, timeout, sse_mode=False)
        )
        
        # 确保返回的是ActionResponse类型
        if isinstance(result, ActionResponse):
            return result
        else:
            # 这种情况不应该发生，但作为安全措施
            return ActionResponse(
                action=Action.RESPONSE,
                result=None,
                response="调用返回了非预期的类型"
            )
    except Exception as e:
        logger.error(f"stdio模式MCP调用封装出错: {str(e)}")
        return ActionResponse(
            action=Action.RESPONSE,
            result=None,
            response=f"stdio模式MCP调用出错: {str(e)}"
        )