<template>
  <div id="app">
    <header>
      <div class="header-content">
        <img src="/icons/financial-advisor.svg" alt="理财助手图标" class="logo">
        <h1>理财助手</h1>
      </div>
    </header>
    <div class="container">
      <!-- 左侧数字人画面 -->
      <div class="avatar-panel">
        <div id="video-container">
          <video id="remote-video" autoplay playsinline style="display: none;"></video>
          <img id="avatar-image" src="/assets/images/aya.png" alt="阿雅数字人">
          <div id="initial-message" style="display: none;">数字人画面区域</div>
        </div>
      </div>

      <!-- 右侧对话框 -->
      <div class="chat-container">
        <div class="tabs">
          <button :class="['tab-button', { active: activeTab === 'chat' }]" @click="activeTab = 'chat'">对话</button>
          <button :class="['tab-button', { active: activeTab === 'products' }]" @click="activeTab = 'products'">理财产品</button>
          <button :class="['tab-button', { active: activeTab === 'advisor' }]" @click="activeTab = 'advisor'">理财咨询</button>
        </div>
        
        <div class="tab-content">
          <!-- 对话Tab -->
          <div v-show="activeTab === 'chat'" class="tab-pane">
            <div class="dialogue-container" ref="dialogueContainer">
              <!-- 错误消息显示 -->
              <div v-if="showError" class="error-message" @click="hideError">
                <i class="fas fa-exclamation-triangle"></i>
                {{ errorMessage }}
                <span class="close-btn">×</span>
              </div>
              
              <div v-if="dialogue.length === 0" class="message role-assistant">
                <div class="message-content">你好，我是阿雅，您的的专属理财助手，有什么可以帮助您？</div>
              </div>
              <div v-for="(message, index) in dialogue" 
                   :key="index" 
                   :class="['message', 'role-' + (message.role || 'system')]">
                <div class="message-content">{{ message.content || '无内容' }}</div>
                <div class="timestamp">{{ formatTime(message.timestamp || Date.now()) }}</div>
                
                <!-- 改进的处理状态指示器 -->
                <div v-if="message.role === 'user' && isProcessing && index === dialogue.length - 1" 
                     class="processing-indicator">
                  <div class="processing-content">
                    <div class="dots">
                      <span></span><span></span><span></span>
                    </div>
                    <span class="processing-text">{{ processingStatus || '正在思考中...' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 固定在底部的输入区域 -->
            <div class="input-area">
              <input type="text" 
                     class="text-input" 
                     v-model="newMessage" 
                     placeholder="请输入您的问题..." 
                     @keyup.enter="sendMessage"
                     autocomplete="off">
              <button class="send-btn" @click="sendMessage" :disabled="!isConnected">发送</button>
              <button :class="['record-btn', {recording: isRecording}]" @click="toggleRecording">
                <i :class="isRecording ? 'fas fa-stop' : 'fas fa-microphone'"></i>
              </button>
              <button class="video-call-btn" @click="startVideoCall" :disabled="!isConnected || isCallActive">
                <i class="fas fa-video"></i>
              </button>
            </div>
          </div>
          
          <!-- 理财产品Tab -->
          <div v-show="activeTab === 'products'" class="tab-pane">
            <div class="products-container">
              <div class="filter-section">
                <h3>筛选条件</h3>
                <div class="filter-group">
                  <label>风险等级：</label>
                  <select v-model="productFilter.riskLevel">
                    <option value="">全部</option>
                    <option value="保守型">保守型</option>
                    <option value="稳健型">稳健型</option>
                    <option value="积极型">积极型</option>
                  </select>
                </div>
                <div class="filter-group">
                  <label>产品类型：</label>
                  <select v-model="productFilter.productType">
                    <option value="">全部</option>
                    <option value="基金">基金</option>
                    <option value="债券">债券</option>
                    <option value="商品">商品</option>
                  </select>
                </div>
                <button @click="fetchProducts" class="refresh-btn">刷新</button>
              </div>
              
              <div class="products-list">
                <div v-if="filteredProducts.length === 0" class="no-products">
                  暂无符合条件的理财产品
                </div>
                <div v-for="product in filteredProducts" :key="product.id" class="product-card">
                  <h4>{{ product.name }}</h4>
                  <div class="product-info">
                    <span class="product-type">{{ product.type }}</span>
                    <span class="risk-level" :class="'risk-' + product.risk_level">{{ product.risk_level }}</span>
                  </div>
                  <p class="expected-return">预期年化收益率：{{ product.expected_return }}%</p>
                  <p class="product-description">{{ product.description }}</p>
                  <button @click="consultProduct(product)" class="consult-btn">咨询此产品</button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 理财咨询Tab -->
          <div v-show="activeTab === 'advisor'" class="tab-pane">
            <div class="advisor-container">
              <div class="advisor-form">
                <h3>理财咨询</h3>
                <div class="form-group">
                  <label>您的问题：</label>
                  <textarea v-model="adviceRequest.question" placeholder="例如：如何配置我的投资组合？" rows="3"></textarea>
                </div>
                <div class="form-group">
                  <label>风险承受能力：</label>
                  <select v-model="adviceRequest.risk_tolerance">
                    <option value="保守型">保守型</option>
                    <option value="稳健型">稳健型</option>
                    <option value="积极型">积极型</option>
                    <option value="激进型">激进型</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>投资金额（元）：</label>
                  <input type="number" v-model.number="adviceRequest.investment_amount" min="1000" placeholder="10000">
                </div>
                <button @click="getFinancialAdvice" class="submit-btn" :disabled="isGettingAdvice">{{ isGettingAdvice ? '正在获取建议...' : '获取理财建议' }}</button>
              </div>
              
              <div v-if="financialAdvice" class="advice-result">
                <h4>理财建议</h4>
                <div class="advice-content">{{ financialAdvice }}</div>
              </div>
              
              <div class="recommendation-form">
                <h3>产品推荐</h3>
                <div class="form-row">
                  <div class="form-group">
                    <label>风险偏好：</label>
                    <select v-model="recommendationRequest.risk_tolerance">
                      <option value="保守型">保守型</option>
                      <option value="稳健型">稳健型</option>
                      <option value="积极型">积极型</option>
                      <option value="激进型">激进型</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>投资期限：</label>
                    <select v-model="recommendationRequest.investment_term">
                      <option value="短期">短期</option>
                      <option value="中期">中期</option>
                      <option value="长期">长期</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label>投资金额（元）：</label>
                    <input type="number" v-model.number="recommendationRequest.amount" min="1000" placeholder="10000">
                  </div>
                </div>
                <button @click="getProductRecommendations" class="submit-btn" :disabled="isGettingRecommendations">{{ isGettingRecommendations ? '正在推荐...' : '获取产品推荐' }}</button>
              </div>
              
              <div v-if="productRecommendations.length > 0" class="recommendations-result">
                <h4>推荐产品</h4>
                <div class="recommended-products">
                  <div v-for="product in productRecommendations" :key="product.id" class="product-card small">
                    <h5>{{ product.name }}</h5>
                    <div class="product-info">
                      <span class="product-type">{{ product.type }}</span>
                      <span class="risk-level" :class="'risk-' + product.risk_level">{{ product.risk_level }}</span>
                    </div>
                    <p class="expected-return">预期年化收益率：{{ product.expected_return }}%</p>
                    <button @click="consultProduct(product)" class="consult-btn small">咨询</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch, computed } from 'vue';
import { WebRTCManager } from './webrtc';

// 定义理财产品类型
interface FinancialProduct {
  id: number;
  name: string;
  type: string;
  risk_level: string;
  expected_return: number;
  description: string;
}

const userId = 'user_' + Math.random().toString(36).substr(2, 9);
let socket: WebSocket | null = null;
let webrtcSocket: WebSocket | null = null;
const isConnected = ref(false);
const reconnectAttempts = ref(0);
const maxReconnectAttempts = 3;
const dialogue = ref<{role?: string; content?: string; timestamp?: number}[]>([]);
const newMessage = ref('');
const isRecording = ref(false);
const connectionStatusElement = ref<HTMLElement | null>(null);
const isCallActive = ref(false);
const isProcessing = ref(false); // 处理状态指示器
const processingStatus = ref(''); // 当前处理状态消息
const errorMessage = ref(''); // 错误消息
const showError = ref(false); // 是否显示错误
let webRTCManager: WebRTCManager | null = null;

// Tab相关状态
const activeTab = ref('chat');

// 理财产品相关状态
const products = ref<FinancialProduct[]>([]);
const productFilter = ref({
  riskLevel: '',
  productType: ''
});
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    if (productFilter.value.riskLevel && product.risk_level !== productFilter.value.riskLevel) {
      return false;
    }
    if (productFilter.value.productType && product.type !== productFilter.value.productType) {
      return false;
    }
    return true;
  });
});

// 理财咨询相关状态
const adviceRequest = ref({
  question: '',
  risk_tolerance: '稳健型',
  investment_amount: 10000
});
const financialAdvice = ref('');
const isGettingAdvice = ref(false);

// 产品推荐相关状态
const recommendationRequest = ref({
  risk_tolerance: '稳健型',
  investment_term: '中期',
  amount: 10000
});
const productRecommendations = ref<FinancialProduct[]>([]);
const isGettingRecommendations = ref(false);

const updateConnectionStatus = (status: string, text: string) => {
  if (connectionStatusElement.value) {
    connectionStatusElement.value.className = 'connection-status ' + status;
    connectionStatusElement.value.textContent = text;
  }
};

// 获取理财产品列表
const fetchProducts = async () => {
  try {
    const response = await fetch('/api/products');
    products.value = await response.json();
  } catch (error) {
    console.error('获取理财产品失败:', error);
    showErrorMessage('获取理财产品失败，请稍后重试');
  }
};

// 咨询特定产品
const consultProduct = (product: any) => {
  activeTab.value = 'chat';
  newMessage.value = `我想了解一下${product.name}这个产品，能给我介绍一下吗？`;
  // 自动发送消息
  setTimeout(() => {
    if (isConnected.value) {
      sendMessage();
    }
  }, 100);
};

// 获取理财建议
const getFinancialAdvice = async () => {
  if (!adviceRequest.value.question.trim()) {
    showErrorMessage('请输入您的问题');
    return;
  }
  
  isGettingAdvice.value = true;
  financialAdvice.value = '';
  
  try {
    const response = await fetch('/api/advice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(adviceRequest.value)
    });
    
    const data = await response.json();
    financialAdvice.value = data.advice;
  } catch (error) {
    console.error('获取理财建议失败:', error);
    showErrorMessage('获取理财建议失败，请稍后重试');
  } finally {
    isGettingAdvice.value = false;
  }
};

// 获取产品推荐
const getProductRecommendations = async () => {
  isGettingRecommendations.value = true;
  productRecommendations.value = [];
  
  try {
    const response = await fetch('/api/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(recommendationRequest.value)
    });
    
    const data = await response.json();
    productRecommendations.value = data.recommendations;
  } catch (error) {
    console.error('获取产品推荐失败:', error);
    showErrorMessage('获取产品推荐失败，请稍后重试');
  } finally {
    isGettingRecommendations.value = false;
  }
};

const connectWebSocket = () => {
  // 如果已达到最大重连次数，停止重连
  if (reconnectAttempts.value >= maxReconnectAttempts) {
    updateConnectionStatus('disconnected', '连接失败，请刷新页面重试');
    // 播放连接失败语音
    speakConnectionFailedMessage();
    return;
  }
  
  const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
  const wsUrl = `${protocol}${window.location.host}/ws?user_id=${userId}`;
  
  try {
    socket = new WebSocket(wsUrl);
    // 播放正在连接语音
    speakConnectingMessage();
    updateConnectionStatus('connecting', '连接中...');
    
    // 连接WebRTC信令服务器
    const webrtcUrl = `${protocol}${window.location.host}/webrtc?user_id=${userId}`;
    webrtcSocket = new WebSocket(webrtcUrl);
    
    socket.onopen = () => {
      console.log('WebSocket连接已建立');
      isConnected.value = true;
      reconnectAttempts.value = 0; // 重置重连次数
      updateConnectionStatus('connected', '已连接');
      
      // 初始化WebRTC客户端
      webRTCManager = new WebRTCManager();
      
      // 连接建立后显示数字人图片
      showAvatar();
      
      // 播放欢迎语音
      speakWelcomeMessage();
    };
    
    // WebRTC信令服务器连接处理
    if (webrtcSocket) {
      webrtcSocket.onopen = () => {
        console.log('WebRTC信令服务器连接已建立');
        
        // 连接WebRTC管理器到信令服务器
        if (webRTCManager) {
          const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
          const webrtcSignalingUrl = `${protocol}${window.location.host}/webrtc?user_id=${userId}`;
          webRTCManager.connectSignalingServer(webrtcSignalingUrl);
        }
      };
      
      webrtcSocket.onmessage = (event) => {
        // 将消息转发给WebRTC管理器
        if (webRTCManager) {
          const message = JSON.parse(event.data);
          webRTCManager.handleSignalingMessage(message);
        }
      };
      
      webrtcSocket.onclose = () => {
        console.log('WebRTC信令服务器连接已断开');
      };
      
      webrtcSocket.onerror = (error) => {
        console.error('WebRTC信令服务器连接错误:', error);
      };
    }
    
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleServerMessage(data);
      } catch (e) {
        console.error('解析服务器消息失败:', e);
      }
    };
    
    socket.onclose = () => {
      console.log('WebSocket连接已断开');
      isConnected.value = false;
      updateConnectionStatus('disconnected', '连接断开');
      
      // 尝试重新连接，增加重连次数
      reconnectAttempts.value++;
      const reconnectDelay = Math.min(1000 * Math.pow(2, reconnectAttempts.value), 10000); // 指数退避，最大10秒
      console.log(`尝试重新连接 (${reconnectAttempts.value}/${maxReconnectAttempts})，${reconnectDelay}ms 后重试`);
      setTimeout(connectWebSocket, reconnectDelay);
    };
    
    // 关闭WebRTC连接
    if (webrtcSocket) {
      webrtcSocket.close();
      webrtcSocket = null;
    }
    if (webRTCManager) {
      webRTCManager.close();
    }
    
    socket.onerror = (error) => {
      console.error('WebSocket错误:', error);
      updateConnectionStatus('disconnected', '连接错误');
    };
  } catch (e) {
    console.error('WebSocket连接失败:', e);
    updateConnectionStatus('disconnected', '连接失败');
    
    // 尝试重新连接
    reconnectAttempts.value++;
    const reconnectDelay = Math.min(1000 * Math.pow(2, reconnectAttempts.value), 10000);
    console.log(`连接失败，${reconnectDelay}ms 后重试 (${reconnectAttempts.value}/${maxReconnectAttempts})`);
    setTimeout(connectWebSocket, reconnectDelay);
  }
};

const handleServerMessage = (data: any) => {
  console.log('收到服务器消息:', data);
  
  switch (data.type) {
    case 'processing_status':
      // 处理状态更新
      isProcessing.value = true;
      processingStatus.value = data.message || '正在处理...';
      console.log('处理状态:', data.status, data.message);
      break;
      
    case 'chat_response':
      // 收到响应时隐藏处理状态
      isProcessing.value = false;
      processingStatus.value = '';
      
      // 处理完整的对话响应
      if (data.dialogue && data.dialogue.length > 0) {
        // 更新对话列表，过滤掉system消息
        dialogue.value = data.dialogue.filter((msg: any) => msg.role !== 'system');
        
        // 如果有助手的回复，优先播放视频而不是系统语音
        const lastMessage = data.dialogue[data.dialogue.length - 1];
        if (lastMessage.role === 'assistant' && lastMessage.content) {
          // 如果没有视频，才使用系统语音
          if (!data.video_url) {
            speakAssistantMessage(lastMessage.content);
          }
        }
      }
      
      // 处理视频播放
      if (data.video_url) {
        playGeneratedVideo(data.video_url);
      }
      
      // 显示处理时间
      if (data.processing_time) {
        console.log(`处理耗时: ${data.processing_time.toFixed(2)}秒`);
      }
      
      break;
      
    case 'error':
      // 处理错误消息
      isProcessing.value = false;
      processingStatus.value = '';
      showErrorMessage(data.data?.error_message || '发生未知错误', data.data?.details);
      break;
      
    case 'update_dialogue':
      // 处理旧版本的对话更新消息（向后兼容）
      if (data.data && data.data.length > 0) {
        const lastMessage = data.data[data.data.length - 1];
        if (lastMessage.role === 'assistant') {
          dialogue.value = [...dialogue.value, lastMessage];
          speakAssistantMessage(lastMessage.content);
        } else {
          dialogue.value = data.data;
        }
      }
      break;
      
    case 'pong':
      // 心跳响应
      console.log('心跳响应');
      break;
      
    case 'offer':
    case 'answer':
    case 'ice-candidate':
      // 处理WebRTC信令消息
      if (webRTCManager) {
        webRTCManager.handleSignalingMessage(data);
      }
      break;
      
    default:
      console.log('未知消息类型:', data.type, data);
  }
};

const showErrorMessage = (message: string, details?: string) => {
  errorMessage.value = message + (details ? ` (${details})` : '');
  showError.value = true;
  // 3秒后自动隐藏错误消息
  setTimeout(() => {
    showError.value = false;
  }, 3000);
};

const hideError = () => {
  showError.value = false;
  errorMessage.value = '';
};

const sendMessage = () => {
  if (!isConnected.value || !newMessage.value.trim()) return;
  
  // 验证输入长度
  if (newMessage.value.trim().length > 500) {
    showErrorMessage('消息太长，请保持在500字以内');
    return;
  }
  
  // 先将用户消息添加到本地对话列表
  const userMessage = {
    role: 'user',
    content: newMessage.value.trim(),
    timestamp: Date.now()
  };
  
  dialogue.value = [...dialogue.value, userMessage];
  
  // 显示处理状态
  isProcessing.value = true;
  processingStatus.value = '正在发送消息...';
  
  // 然后发送消息到后端
  const message = {
    type: 'message',
    role: 'user',
    content: newMessage.value.trim(),
    timestamp: Date.now()
  };
  
  try {
    socket!.send(JSON.stringify(message));
    newMessage.value = '';
    
    // 设置超时处理
    setTimeout(() => {
      if (isProcessing.value) {
        isProcessing.value = false;
        processingStatus.value = '';
        showErrorMessage('处理超时，请稍后重试');
      }
    }, 120000); // 1分钟超时
    
  } catch (e) {
    console.error('发送消息失败:', e);
    showErrorMessage('发送消息失败，请检查网络连接');
    // 发送失败时隐藏处理状态
    isProcessing.value = false;
    processingStatus.value = '';
  }
};

const toggleRecording = () => {
  isRecording.value = !isRecording.value;
  // 这里可以添加实际的录音逻辑
};

const showAvatar = () => {
  // 显示数字人图片
  const avatarImage = document.getElementById('avatar-image');
  const initialMessage = document.getElementById('initial-message');
  
  if (avatarImage && initialMessage) {
    initialMessage.style.display = 'none';
    avatarImage.style.display = 'block';
  }
};

const speakWelcomeMessage = () => {
  // 创建音频上下文播放欢迎语音
  const welcomeText = "你好，我是阿雅，您的专属理财助手，有什么可以帮助您？";
  const utterance = new SpeechSynthesisUtterance(welcomeText);
  utterance.lang = 'zh-CN';
  utterance.rate = 1;
  utterance.pitch = 1;
  speechSynthesis.speak(utterance);
};

const speakAssistantMessage = (message: string) => {
  // 创建音频上下文播放助手回复语音
  const utterance = new SpeechSynthesisUtterance(message);
  utterance.lang = 'zh-CN';
  utterance.rate = 1;
  utterance.pitch = 1;
  speechSynthesis.speak(utterance);
};

const speakConnectingMessage = () => {
  // 创建音频上下文播放正在连接语音
  const message = "正在为你联系理财助手阿雅，请稍后";
  const utterance = new SpeechSynthesisUtterance(message);
  utterance.lang = 'zh-CN';
  utterance.rate = 1;
  utterance.pitch = 1;
  speechSynthesis.speak(utterance);
};

const speakConnectionFailedMessage = () => {
  // 创建音频上下文播放连接失败语音
  const message = "连接失败，请刷新页面重试";
  const utterance = new SpeechSynthesisUtterance(message);
  utterance.lang = 'zh-CN';
  utterance.rate = 1;
  utterance.pitch = 1;
  speechSynthesis.speak(utterance);
};

const playGeneratedVideo = (videoUrl: string) => {
  const remoteVideo = document.getElementById('remote-video') as HTMLVideoElement;
  const avatarImage = document.getElementById('avatar-image') as HTMLImageElement;
  
  if (remoteVideo && avatarImage) {
    // 设置视频源
    remoteVideo.src = videoUrl;
    
    // 显示视频，隐藏静态图片
    remoteVideo.style.display = 'block';
    avatarImage.style.display = 'none';
    
    // 播放视频
    remoteVideo.play().catch(error => {
      console.error('视频播放失败:', error);
      // 如果播放失败，显示静态图片
      remoteVideo.style.display = 'none';
      avatarImage.style.display = 'block';
    });
    
    // 视频播放结束后显示静态图片
    remoteVideo.onended = () => {
      remoteVideo.style.display = 'none';
      avatarImage.style.display = 'block';
    };
  }
};

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString();
};

const startVideoCall = async () => {
  if (!webRTCManager) return;
  
  try {
    isCallActive.value = true;
    await webRTCManager.startCall();
  } catch (error) {
    console.error('启动视频通话失败:', error);
    isCallActive.value = false;
    alert('启动视频通话失败，请重试');
  }
};

onMounted(() => {
  // 创建连接状态显示元素
  connectionStatusElement.value = document.createElement('div');
  connectionStatusElement.value.id = 'connection-status';
  connectionStatusElement.value.className = 'connection-status connecting';
  connectionStatusElement.value.textContent = '连接中...';
  document.body.appendChild(connectionStatusElement.value);
  
  // 连接WebSocket
  connectWebSocket();
  
  // 获取理财产品列表
  fetchProducts();
  
  // 每30秒发送一次心跳包
  // setInterval(sendPing, 30000);
});

watch(dialogue, () => {
  // 在对话更新时滚动到底部
  nextTick(() => {
    const container = document.querySelector('.dialogue-container');
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  });
});
</script>

<style>
:root {
  --primary-color: #007bff;
  --user-message-bg: #e8f5e9;
  --user-message-border: #c8e6c9;
  --user-message-color: #2e7d32;
  --assistant-message-bg: #fff3e0;
  --assistant-message-border: #ffe0b2;
  --assistant-message-color: #f57c00;
  --system-message-bg: #eceff1;
  --system-message-border: #cfd8dc;
  --system-message-color: #37474f;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #e2e2e2 0%, #ffffff 100%);
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* 连接状态 */
.connection-status {
  position: fixed;
  top: 10px;
  right: 20px;
  padding: 5px 10px;
  border-radius: 10px;
  color: white;
  font-size: 12px;
  z-index: 1000;
  transition: all 0.3s ease;
}

.connected {
  background-color: #4caf50;
}

.disconnected {
  background-color: #f44336;
}

.connecting {
  background-color: #ff9800;
}

/* 头部 */
header {
  background: linear-gradient(135deg, #007bff, #0069d9);
  color: white;
  padding: 5px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: none;
  border-radius: 5px;
  margin: 0 auto;
  max-width: 1800px;
  width: 100%;
}

/* Tabs */
.tabs {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f8f9fa;
}

.tab-button {
  padding: 12px 24px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: all 0.3s;
  border-bottom: 3px solid transparent;
}

.tab-button:hover {
  color: #007bff;
  background-color: #e9ecef;
}

.tab-button.active {
  color: #007bff;
  border-bottom: 3px solid #007bff;
  background-color: #fff;
}

.tab-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 头部内容 */
.header-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
  border-radius: 20px;
}

.logo {
  height: 36px;
  width: auto;
  margin-right: 12px;
}

h1 {
  margin: 0;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 1px;
}

/* 主容器 */
.container {
  flex: 1;
  display: flex;
  max-width: 1800px;
  margin: 5px auto;
  height: calc(100vh - 100px);
  gap: 16px;
  padding: 0 0px;
  width: 100%;
}

/* 左侧数字人画面 */
.avatar-panel {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 10px;
  position: relative;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 视频容器 */
#video-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

/* 数字人图片 */
#avatar-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 10px;
}

/* 远程视频 */
#remote-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 10px;
}

/* 右侧对话框区域 */
.chat-container {
  flex: 2;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  height: 100%;
}

/* 对话框容器 */
.dialogue-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  /* 隐藏滚动条 */
  scrollbar-width: none;
  -ms-overflow-style: none;
}

/* Tab面板 */
.tab-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.dialogue-container::-webkit-scrollbar {
  display: none;
}

.message {
  position: relative;
  transition: background 0.3s, transform 0.2s;
  display: flex;
  flex-direction: column;
  padding: 12px 16px;
  border-radius: 18px;
  max-width: 80%;
  word-wrap: break-word;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.role-user {
  color: var(--user-message-color);
  align-self: flex-start;
  background-color: var(--user-message-bg);
  border: 1px solid var(--user-message-border);
  border-bottom-left-radius: 5px;
}

.message.role-assistant {
  color: var(--assistant-message-color);
  align-self: flex-end;
  background-color: var(--assistant-message-bg);
  border: 1px solid var(--assistant-message-border);
  border-bottom-right-radius: 5px;
}

.message.role-system {
  color: var(--system-message-color);
  align-self: center;
  text-align: center;
  background-color: var(--system-message-bg);
  border: 1px solid var(--system-message-border);
  max-width: 100%;
}

.message-content {
  font-size: 16px;
  line-height: 1.5;
}

.timestamp {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

/* 错误消息样式 */
.error-message {
  background-color: #ffe6e6;
  border: 1px solid #ff9999;
  border-radius: 8px;
  color: #cc0000;
  padding: 12px 16px;
  margin: 10px 0;
  display: flex;
  align-items: center;
  cursor: pointer;
  animation: slideIn 0.3s ease-out;
  position: relative;
}

.error-message i {
  margin-right: 8px;
  font-size: 16px;
}

.error-message .close-btn {
  margin-left: auto;
  font-size: 18px;
  font-weight: bold;
  opacity: 0.7;
}

.error-message:hover {
  background-color: #ffd6d6;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 处理状态指示器优化 */
.processing-indicator {
  margin-top: 8px;
  color: #666;
  font-size: 13px;
  background-color: #f8f9fa;
  padding: 8px 12px;
  border-radius: 15px;
  border: 1px solid #e9ecef;
}

.processing-content {
  display: flex;
  align-items: center;
}

.dots {
  display: flex;
  gap: 3px;
  margin-right: 8px;
}

.dots span {
  width: 4px;
  height: 4px;
  background-color: #007bff;
  border-radius: 50%;
  animation: dot-bounce 1.4s infinite ease-in-out;
}

.dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dot-bounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

.processing-text {
  font-style: italic;
}

/* 文字输入框 */
.input-area {
  display: flex;
  gap: 10px;
  padding: 20px;
  background: white;
  border-top: 1px solid #eee;
}

/* 理财产品样式 */
.products-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.filter-section {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}

.filter-section h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-weight: 500;
  color: #555;
}

.filter-group select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.refresh-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.refresh-btn:hover {
  background: #0069d9;
}

.products-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.no-products {
  text-align: center;
  color: #666;
  padding: 40px;
  font-size: 18px;
}

.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.product-card.small {
  padding: 15px;
}

.product-card h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
}

.product-card h5 {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 16px;
}

.product-info {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.product-type {
  background: #e9ecef;
  color: #495057;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.risk-level {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.risk-保守型 {
  background: #d4edda;
  color: #155724;
}

.risk-稳健型 {
  background: #cce7ff;
  color: #004085;
}

.risk-积极型 {
  background: #fff3cd;
  color: #856404;
}

.risk-激进型 {
  background: #f8d7da;
  color: #721c24;
}

.expected-return {
  font-weight: 600;
  color: #28a745;
  margin: 10px 0;
}

.product-description {
  color: #666;
  margin: 10px 0;
  line-height: 1.5;
}

.consult-btn {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 10px;
}

.consult-btn.small {
  padding: 6px 12px;
  font-size: 14px;
  margin-top: 8px;
}

.consult-btn:hover {
  background: #0069d9;
}

/* 理财咨询样式 */
.advisor-container {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.advisor-form, .recommendation-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.advisor-form h3, .recommendation-form h3 {
  margin-top: 0;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.form-group textarea, .form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-row {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.form-row .form-group {
  flex: 1;
  min-width: 200px;
}

.submit-btn {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 16px;
  font-weight: 500;
}

.submit-btn:hover:not(:disabled) {
  background: #0069d9;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.advice-result, .recommendations-result {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.advice-result h4, .recommendations-result h4 {
  margin-top: 0;
  color: #333;
}

.advice-content {
  line-height: 1.6;
  color: #555;
}

.recommended-products {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.text-input {
  flex: 1;
  padding: 12px 20px;
  border: 1px solid #ddd;
  border-radius: 25px;
  outline: none;
  font-size: 16px;
}

.text-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.send-btn {
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.3s;
  font-weight: 500;
}

.send-btn:hover {
  background: #0069d9;
}

.send-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.record-btn, .video-call-btn {
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s;
}

.record-btn:hover, .video-call-btn:hover {
  background: #0069d9;
}

.record-btn.recording {
  background: #ff5722;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 87, 34, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(255, 87, 34, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 87, 34, 0); }
}

h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #888;
  margin-top: 20px;
  padding: 20px;
}

@media (max-width: 992px) {
  .container {
    flex-direction: column;
    height: auto;
    margin: 10px;
    padding: 0;
  }
  
  .avatar-panel {
    width: 100%;
    height: 200px;
  }
  
  .dialogue-container {
    height: 500px;
  }
}

@media (max-width: 600px) {
  .dialogue-container {
    padding: 10px;
    height: 400px;
  }
  
  .message-content {
    font-size: 14px;
  }
  
  .input-area {
    padding: 10px;
  }
  
  .text-input {
    padding: 10px 15px;
    font-size: 14px;
  }
  
  .send-btn, .record-btn, .video-call-btn {
    padding: 10px 20px;
  }
}
</style>