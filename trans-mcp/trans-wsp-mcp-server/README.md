# trans-wsp-mcp-server

财富管理查询服务模块，基于Python MCP SDK构建，使用streamablehttp方式暴露服务。

## 功能特性

- 财富产品查询
- 投资组合分析
- 风险评估查询
- 收益预测计算

## 环境管理

本项目使用 Miniconda 管理环境，环境名称为 `trans-wsp-mcp`。

### 创建环境

```bash
conda create -n trans-wsp-mcp python=3.8 -y
```

### 激活环境

```bash
conda activate trans-wsp-mcp
```

或者使用项目提供的脚本：

```bash
./activate_env.sh
```

### 退出环境

```bash
conda deactivate
```

## 安装依赖

在激活的环境中安装依赖：

```bash
pip install -r requirements.txt
```

注意：如果 `mcp` 是自定义SDK，则需要单独安装：
```bash
# 从源码安装
pip install -e /path/to/mcp/sdk

# 或从git仓库安装
pip install git+https://github.com/your-org/mcp-sdk.git
```

## 运行服务

### 方法1：直接运行
```bash
python src/main.py
```

### 方法2：使用启动脚本
```bash
./start_server.sh
```

## MCP服务端点

- MCP服务端点: `/mcp`
- 健康检查端点: `/health`

## 支持的工具

1. `query_financial_products` - 查询可投资的金融产品
2. `analyze_portfolio` - 分析投资组合表现
3. `assess_risk` - 评估投资风险
4. `predict_returns` - 预测投资收益

## 支持的资源

1. `db://wealth/products` - 金融产品数据库
2. `db://wealth/portfolios/{portfolio_id}` - 投资组合数据

## 支持的提示词

1. `wealth_advice` - 根据用户情况提供财富管理建议