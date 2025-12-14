# 虚拟柜员理财助手平台

虚拟柜员理财助手平台是一个集成了语音交互、AI技术和WebRTC视频通话功能的综合性金融服务平台。该平台基于现有的工程结构构建，提供专业的理财咨询服务、个性化的产品推荐以及实时的语音视频交互体验。

## 🌟 平台特性

- 🎤 **实时语音交互**: 支持语音输入和语音输出，提供自然的对话体验
- 🎥 **WebRTC视频通话**: 集成数字人技术，实现生动的视频交互
- 🏦 **专业理财服务**: 提供投资建议、资产配置和产品推荐
- 🧠 **AI智能助手**: 基于大语言模型，具备强大的理解和对话能力
- 📱 **现代化界面**: 响应式设计，支持多设备访问
- 🔧 **模块化架构**: 易于扩展和定制的功能模块

## 🏗️ 项目结构

```
.
├── trans-mcp/              # MCP服务端（微服务通信协议）
├── trans-stv/              # 语音处理核心系统（后端）
│   ├── config/             # 配置文件
│   ├── documents/          # 文档资料
│   ├── models/             # AI模型
│   ├── plugins/            # 插件系统
│   ├── src/                # 核心源代码
│   └── third_party/        # 第三方库
└── trans-vtw/              # Web前端界面
    ├── src/                # 前端源代码
    └── public/             # 静态资源
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 7+

### 安装依赖

```bash
# 安装后端依赖
cd trans-stv
pip install -r requirements.txt
pip install -r third_party/OpenManus/requirements.txt 
conda install ffmpeg

# 安装前端依赖
cd ../trans-vtw
npm install
```

### 配置环境

1. 打开 `trans-stv/config/config.yaml` 配置ASR、LLM等相关配置
2. 下载必要的模型文件：
   - SenseVoiceSmall到目录 `trans-stv/models/SenseVoiceSmall`
   - bge-small-zh到目录 `trans-stv/models/bge-small-zh`
3. 配置大语言模型API密钥（如deepseek、openai等）

### 启动服务

```bash
# 方法一：分别启动前后端服务
cd trans-stv
./start_server.sh  # 启动后端服务

# 在另一个终端中启动前端服务
cd ../trans-vtw
npm run dev

# 方法二：一键启动所有服务
cd ..
./start_all.sh

# 方法三：优化版一键启动（推荐）
./start_optimized.sh
```

### 访问平台

启动完成后，在浏览器中访问 `http://localhost:3000`

## 🛠️ 核心功能模块

### 1. 语音交互系统 (trans-stv)
- **语音识别** (ASR): 将用户的语音转换为文本
- **语音合成** (TTS): 将文本回复转换为语音
- **语音活动检测** (VAD): 检测语音活动，区分语音和静音
- **大语言模型** (LLM): 处理用户输入并生成智能回复
- **数字人生成** (THG): 通过SadTalker生成数字人视频

### 2. 理财服务模块
- **理财咨询**: 提供专业的投资建议和资产配置方案
- **产品推荐**: 根据用户需求推荐合适的理财产品
- **风险评估**: 协助用户了解不同产品的风险特征

### 3. Web前端界面 (trans-vtw)
- **实时通信**: 通过WebSocket与后端保持实时连接
- **视频播放**: 展示数字人形象和视频内容
- **多标签界面**: 对话、理财产品、理财咨询等功能模块

## 🔧 性能优化

为了获得最佳性能，建议使用以下优化配置：

1. 使用优化配置文件：`trans-stv/config/optimized_config.yaml`
2. 选择性能较好的模型：如 `qwen2:1.5b`
3. 启用工具调用和中断功能以提升交互体验
4. 使用EdgeTTS以获得更快的语音合成速度

## 📖 使用指南

### 基本对话
用户可以通过语音或文字与虚拟柜员进行对话，询问各种问题，包括但不限于：
- 日常问候和闲聊
- 天气查询
- 时间查询
- 网络搜索
- 理财咨询

### 理财服务
1. **理财产品浏览**: 在前端界面的"理财产品"标签页中浏览和筛选产品
2. **理财咨询**: 在"理财咨询"标签页中填写问题和需求，获取专业建议
3. **产品推荐**: 根据个人风险偏好和投资目标获取个性化产品推荐

### 视频通话
点击界面上的视频通话按钮，可以启动WebRTC视频通话功能，与数字人进行面对面的交流。

## 🔧 开发指南

### 添加新功能
1. 后端功能扩展：在 `trans-stv/plugins/functions/` 目录下添加新的插件函数
2. 前端界面扩展：在 `trans-vtw/src/App.vue` 中添加新的UI组件
3. 配置更新：在 `trans-stv/plugins/function_calls_config.json` 中添加新的函数定义

### 自定义模型
平台支持多种AI模型的替换和扩展：
- ASR模型：可替换为其他语音识别模型
- LLM模型：支持多种大语言模型（deepseek、qwen、gemini等）
- TTS模型：支持多种语音合成技术

## 🤝 贡献

欢迎提交Issue和Pull Request来改进虚拟柜员理财助手平台。

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

## 📞 联系我们

如有任何问题或建议，请通过以下方式联系我们：
- 邮箱：support@aya-finance.com
- GitHub Issues：[提交问题](https://github.com/your-repo/issues)

我们会不断改进平台功能，为您提供更好的服务体验。