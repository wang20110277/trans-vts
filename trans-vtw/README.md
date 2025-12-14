# Trans-VTW 前端应用

Trans-VTS数字人对话系统的前端界面，基于Vue 3 + TypeScript构建。

## 🌟 特性

- 🎨 **现代化界面**: 基于Vue 3 Composition API
- 📱 **响应式设计**: 支持多设备适配
- 🌐 **WebSocket通信**: 实时与后端通信
- 🎥 **视频播放**: 支持数字人视频播放
- 💬 **聊天界面**: 直观的对话交互界面
- 🏦 **理财功能**: 专业的理财咨询和产品推荐
- ⚡ **快速开发**: Vite构建工具，热重载支持

## 🚀 快速开始

### 环境要求
- Node.js >= 16
- npm >= 7

### 安装依赖
```bash
npm install
```

### 开发模式
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

### 预览生产版本
```bash
npm run preview
```

## 🏗️ 项目结构

```
src/
├── App.vue          # 主应用组件
├── main.ts          # 应用入口
└── webrtc.ts        # WebRTC通信模块
```

## 📡 WebSocket通信

### 连接配置
- 开发环境: `ws://127.0.0.1:8000/ws`
- 代理配置: `vite.config.ts`

### 消息处理
- 发送聊天消息
- 接收AI响应
- 显示处理状态
- 播放生成视频

## 🎨 界面功能

### 聊天界面
- 用户消息输入
- 消息历史显示
- 实时状态指示

### 理财功能
- 理财产品浏览和筛选
- 个性化理财建议
- 专业产品推荐

### 视频播放
- 数字人视频播放
- 自动播放控制
- 错误处理

## ⚙️ 配置说明

### Vite配置 (`vite.config.ts`)
```typescript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/ws': {
        target: 'ws://127.0.0.1:8000',
        ws: true,
      },
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
```

## 🔧 开发指南

### 添加新功能
1. 在`src/`目录创建组件
2. 在`App.vue`中导入使用
3. 配置路由(如需要)

### WebSocket事件处理
```typescript
// 发送消息
websocket.send(JSON.stringify({
  type: 'chat_message',
  data: { text: userInput }
}))

// 接收消息
websocket.onmessage = (event) => {
  const message = JSON.parse(event.data)
  handleMessage(message)
}
```

## 🛠️ 技术栈

- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript
- **Vite**: 快速构建工具
- **WebSocket**: 实时通信
- **CSS3**: 样式设计

## 📱 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

---

更多信息请参考 [Trans-VTS 主项目文档](../README.md)