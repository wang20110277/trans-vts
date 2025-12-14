#!/bin/bash

# 启动虚拟柜员理财助手平台的所有服务

echo "========================================="
echo "  启动虚拟柜员理财助手平台"
echo "========================================="

# 启动后端服务
echo "启动后端服务..."
cd trans-stv
./start_server.sh &
BACKEND_PID=$!
cd ..

# 等待后端服务启动
sleep 5

# 启动前端服务
echo "启动前端服务..."
cd trans-vtw
npm run dev &
FRONTEND_PID=$!
cd ..

# 显示访问信息
echo "========================================="
echo "服务启动完成！"
echo "后端服务 PID: $BACKEND_PID"
echo "前端服务 PID: $FRONTEND_PID"
echo ""
echo "请在浏览器中访问以下地址："
echo "http://localhost:3000"
echo "========================================="

# 等待用户按键停止服务
echo "按 Ctrl+C 停止所有服务"
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait