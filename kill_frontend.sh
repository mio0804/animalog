#!/bin/bash

# フロントエンドプロセスを安全に停止するスクリプト

echo "Stopping frontend processes..."

# viteプロセスを停止
ps aux | grep -v grep | grep "vite" | awk '{print $2}' | xargs -r kill -9 2>/dev/null

# npm dev プロセスを停止  
ps aux | grep -v grep | grep "npm.*dev" | awk '{print $2}' | xargs -r kill -9 2>/dev/null

# node viteプロセスを停止
ps aux | grep -v grep | grep "node.*vite" | awk '{print $2}' | xargs -r kill -9 2>/dev/null

echo "Frontend processes stopped"

# 残っているプロセスを確認
echo "Remaining processes:"
ps aux | grep -E "(vite|npm.*dev)" | grep -v grep | head -5 || echo "No active processes found"