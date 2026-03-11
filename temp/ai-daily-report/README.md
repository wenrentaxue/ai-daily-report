# AI Daily Report 🤖

每日 AI 新闻自动汇总系统

## 功能

- ✅ 每天 8 点自动收集 AI 新闻
- ✅ 使用 Tavily API 搜索
- ✅ AI 翻译成中文
- ✅ 自动分类整理
- ✅ 生成静态网站
- ✅ 自动发布到 GitHub Pages

## 架构

```
OpenClaw (定时任务)
    ↓
Tavily API (新闻搜索)
    ↓
AI 模型 (翻译 + 摘要)
    ↓
HTML 生成
    ↓
GitHub Pages (发布)
```

## 安装

```bash
# 1. 克隆到 GitHub
git init
git remote add origin https://github.com/your-username/ai-daily-report.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 GitHub Pages
# Settings → Pages → Source: GitHub Actions
```

## 使用

### 手动运行

```bash
cd ~/.openclaw/workspace/projects/ai-daily-report

# 收集新闻
python3 src/collector.py

# 生成报告
python3 src/generator.py

# 提交发布
git add output/
git commit -m "Daily report: $(date +%Y-%m-%d)"
git push
```

### 自动运行

OpenClaw 定时任务每天 8 点自动执行

## 配置

编辑 `config.json`:
- `search_queries`: 搜索关键词
- `max_results`: 最大结果数
- `schedule`: 执行时间

## 输出

- `output/index.html` - 网站首页
- `output/archive/YYYY-MM-DD.md` - 历史归档

## 访问

https://wenrentaxue.github.io/ai-daily-report/

---

Powered by OpenClaw + Tavily
