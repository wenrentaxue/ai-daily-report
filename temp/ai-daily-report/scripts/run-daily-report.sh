#!/bin/bash
# AI Daily Report - 每日执行脚本
# 由 OpenClaw 定时任务调用

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_DIR/src"
OUTPUT_DIR="$PROJECT_DIR/output"

echo "=== AI Daily Report ==="
echo "Time: $(date)"
echo "Project: $PROJECT_DIR"

# 1. 收集新闻
echo ""
echo "📰 Step 1: Collecting AI news..."
cd "$SRC_DIR"
python3 collector.py

# 2. 生成日报（需要 AI 翻译）
echo ""
echo "🤖 Step 2: Generating daily report (with AI translation)..."
# 这里会调用 OpenClaw 的 AI 能力进行翻译
# 实际执行通过 sessions_spawn 调用 AI Agent

# 3. 提交到 Git
echo ""
echo "📦 Step 3: Committing to Git..."
cd "$PROJECT_DIR"

TODAY=$(date +%Y-%m-%d)

git add output/
if git diff --staged --quiet; then
    echo "No changes to commit"
else
    git commit -m "Daily report: $TODAY"
    git push origin main
    echo "✅ Pushed to GitHub"
fi

echo ""
echo "=== Complete ==="
echo "View at: https://wenrentaxue.github.io/ai-daily-report/"
