# 部署指南

## 第一次部署（手动）

### 1. 创建 GitHub 仓库

访问：https://github.com/new

- **Repository name**: `ai-daily-report`
- **Description**: AI Daily Report - 每日 AI 新闻自动汇总
- **Visibility**: Public（公开）
- **不要** 勾选 "Add a README file"
- **不要** 勾选 ".gitignore"
- **不要** 选择 license

点击 **Create repository**

### 2. 推送代码

仓库创建后，在终端执行：

```bash
cd ~/.openclaw/workspace/projects/ai-daily-report

# 推送代码
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 进入仓库页面：https://github.com/wenrentaxue/ai-daily-report
2. 点击 **Settings**（设置）
3. 左侧菜单点击 **Pages**
4. **Source** 选择：**GitHub Actions**
5. 点击 **Save**

### 4. 等待部署

等待 1-2 分钟，GitHub Actions 会自动运行：

1. 进入 **Actions** 标签页
2. 查看部署进度
3. 完成后会显示绿色 ✅

### 5. 访问网站

部署完成后，访问：

**https://wenrentaxue.github.io/ai-daily-report/**

---

## 后续自动部署

每天 8:00 后，系统会自动：

1. 收集 AI 新闻
2. AI 翻译并生成报告
3. 提交代码到 Git
4. 自动推送到 GitHub
5. GitHub Actions 自动部署

**无需人工介入！**

---

## 故障排查

### 推送失败

```bash
# 检查远程仓库
git remote -v

# 如果不对，删除重新添加
git remote remove origin
git remote add origin https://github.com/wenrentaxue/ai-daily-report.git

# 重新推送
git push -u origin main
```

### GitHub Actions 失败

1. 进入 **Actions** 标签页
2. 点击失败的 run
3. 查看错误日志
4. 常见问题：
   - 分支名不对（应该是 `main`）
   - Pages 配置不对（应该选 `GitHub Actions`）

---

## 自定义配置

### 修改关注领域

编辑 `config.json` 中的 `search_queries`

### 修改执行时间

OpenClaw 定时任务配置在 cron 中

### 修改网站样式

编辑 `src/generator.py` 中的 HTML 模板

---

**祝你使用愉快！** 🎉
