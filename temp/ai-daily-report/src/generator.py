#!/usr/bin/env python3
"""
AI 日报生成器 - 翻译、摘要、生成 HTML
"""

import json
import os
from pathlib import Path
from datetime import datetime
from jinja2 import Template

SCRIPT_DIR = Path(__file__).parent.parent

def translate_and_summarize(articles):
    """
    使用 AI 翻译并摘要新闻
    
    返回格式：
    [
      {
        "title_cn": "中文标题",
        "content_cn": "中文摘要",
        "url": "原文链接",
        "source": "来源",
        "category": "分类"
      }
    ]
    """
    # 这里通过 OpenClaw 调用 AI 模型进行翻译
    # 实际执行时会通过 sessions_spawn 调用 AI
    
    processed = []
    
    for article in articles:
        # 简化处理：提取关键信息
        processed.append({
            "title_cn": article.get("title", "无标题"),  # 待 AI 翻译
            "content_cn": article.get("content", "")[:200] + "...",  # 待 AI 翻译
            "url": article.get("url", ""),
            "source": extract_source(article.get("url", "")),
            "original_title": article.get("title", ""),
            "original_content": article.get("content", "")
        })
    
    return processed

def extract_source(url):
    """从 URL 提取来源"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain.split(".")[0].title()
    except:
        return "Unknown"

def categorize_articles(articles):
    """将文章分类"""
    categories = {
        "技术突破": [],
        "产品发布": [],
        "投资融资": [],
        "行业动态": [],
    }
    
    keywords = {
        "技术突破": ["research", "breakthrough", "model", "algorithm", "paper"],
        "产品发布": ["launch", "product", "release", "beta", "announcement"],
        "投资融资": ["funding", "investment", "raised", "series", "million"],
        "行业动态": ["industry", "market", "regulation", "policy", "partnership"],
    }
    
    for article in articles:
        text = (article.get("original_title", "") + " " + 
                article.get("original_content", "")).lower()
        
        categorized = False
        for category, kws in keywords.items():
            if any(kw in text for kw in kws):
                categories[category].append(article)
                categorized = True
                break
        
        if not categorized:
            categories["行业动态"].append(article)
    
    # 过滤空分类
    return {k: v for k, v in categories.items() if v}

def generate_daily_summary(processed_articles, categories):
    """生成日报汇总文本"""
    today = datetime.now().strftime("%Y 年 %m 月 %d 日")
    weekday = datetime.now().strftime("%A")
    
    summary = f"""# AI 每日简报

**日期**: {today} ({weekday})
**生成时间**: {datetime.now().strftime("%H:%M")}
**收录新闻**: {len(processed_articles)} 篇

---

## 📊 今日概览

"""
    
    for category, articles in categories.items():
        summary += f"- **{category}**: {len(articles)} 篇\n"
    
    summary += "\n---\n\n"
    
    for category, articles in categories.items():
        summary += f"## {category}\n\n"
        for i, article in enumerate(articles, 1):
            summary += f"### {i}. {article['title_cn']}\n\n"
            summary += f"{article['content_cn']}\n\n"
            summary += f"📎 [阅读原文]({article['url']}) | 来源：{article['source']}\n\n"
        summary += "---\n\n"
    
    return summary

def generate_html(summary_text, articles, categories):
    """生成 HTML 页面"""
    
    template_str = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily Report - {{ date }}</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6; 
            color: #333; 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 20px;
            background: #f5f5f7;
        }
        .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); }
        h1 { color: #1a1a1a; margin-bottom: 10px; font-size: 2em; }
        .meta { color: #666; font-size: 0.9em; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
        h2 { color: #2c3e50; margin: 30px 0 15px; padding-bottom: 10px; border-bottom: 2px solid #3498db; }
        h3 { color: #34495e; margin: 20px 0 10px; font-size: 1.1em; }
        .category { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .article { margin: 20px 0; padding: 15px; background: #fafafa; border-radius: 6px; border-left: 4px solid #3498db; }
        .article p { margin: 10px 0; color: #555; }
        .article a { color: #3498db; text-decoration: none; }
        .article a:hover { text-decoration: underline; }
        .source { font-size: 0.85em; color: #888; }
        .overview { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
        .overview-item { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .overview-item .count { font-size: 2em; font-weight: bold; }
        .overview-item .label { font-size: 0.85em; opacity: 0.9; }
        footer { text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 0.85em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Daily Report</h1>
        <div class="meta">
            <strong>日期:</strong> {{ date }} | 
            <strong>生成时间:</strong> {{ time }} | 
            <strong>收录新闻:</strong> {{ total }} 篇
        </div>
        
        <h2>📊 今日概览</h2>
        <div class="overview">
            {% for cat, count in overview.items() %}
            <div class="overview-item">
                <div class="count">{{ count }}</div>
                <div class="label">{{ cat }}</div>
            </div>
            {% endfor %}
        </div>
        
        {% for category, articles in categories.items() %}
        <div class="category">
            <h2>{{ category }}</h2>
            {% for article in articles %}
            <div class="article">
                <h3>{{ article.title_cn }}</h3>
                <p>{{ article.content_cn }}</p>
                <p class="source">
                    📎 <a href="{{ article.url }}" target="_blank" rel="noopener">阅读原文</a> | 
                    来源：{{ article.source }}
                </p>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
        
        <footer>
            <p>Generated by AI Daily Report | Powered by OpenClaw + Tavily</p>
        </footer>
    </div>
</body>
</html>
"""
    
    template = Template(template_str)
    
    overview = {cat: len(arts) for cat, arts in categories.items()}
    
    html = template.render(
        date=datetime.now().strftime("%Y 年 %m 月 %d 日"),
        time=datetime.now().strftime("%H:%M"),
        total=len(articles),
        overview=overview,
        categories=categories
    )
    
    return html

def main():
    """主函数"""
    # 读取原始新闻
    raw_dir = SCRIPT_DIR / "output" / "raw"
    today = datetime.now().strftime("%Y-%m-%d")
    raw_file = raw_dir / f"{today}-raw.json"
    
    if not raw_file.exists():
        print(f"Raw news file not found: {raw_file}")
        print("Run collector.py first!")
        return
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    articles = data.get("articles", [])
    print(f"Loaded {len(articles)} articles")
    
    # 翻译和摘要（这里简化处理，实际应该调用 AI）
    processed = translate_and_summarize(articles)
    
    # 分类
    categories = categorize_articles(processed)
    
    # 生成日报汇总
    summary = generate_daily_summary(processed, categories)
    
    # 保存汇总
    archive_dir = SCRIPT_DIR / "output" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    summary_file = archive_dir / f"{today}.md"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"Saved summary to {summary_file}")
    
    # 生成 HTML
    html = generate_html(summary, processed, categories)
    html_file = SCRIPT_DIR / "output" / "index.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated HTML: {html_file}")

if __name__ == "__main__":
    main()
