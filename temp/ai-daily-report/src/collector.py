#!/usr/bin/env python3
"""
AI 新闻收集器 - 使用 Tavily API 搜索最新 AI 新闻
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.parent
TAVILY_SCRIPT = Path.home() / ".openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py"

def search_ai_news(max_results=10):
    """使用 Tavily 搜索 AI 新闻"""
    
    queries = [
        "artificial intelligence AI news today latest",
        "AI machine learning breakthrough research 2026",
        "AI startup funding investment news",
        "AI product launch new technology",
    ]
    
    all_results = []
    
    for query in queries:
        print(f"Searching: {query}")
        
        cmd = [
            "python3", str(TAVILY_SCRIPT),
            "--query", query,
            "--max-results", str(max_results // len(queries)),
            "--format", "raw"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            for item in data.get("results", []):
                item["search_query"] = query
                all_results.append(item)
        else:
            print(f"Search failed: {result.stderr}")
    
    # 去重（基于 URL）
    seen_urls = set()
    unique_results = []
    for item in all_results:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(item)
    
    print(f"Found {len(unique_results)} unique articles")
    return unique_results

def save_raw_news(results, output_dir):
    """保存原始新闻数据"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"{today}-raw.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "date": today,
            "collected_at": datetime.now().isoformat(),
            "count": len(results),
            "articles": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Saved raw news to {output_file}")
    return output_file

if __name__ == "__main__":
    output_dir = SCRIPT_DIR / "output" / "raw"
    results = search_ai_news(max_results=10)
    save_raw_news(results, output_dir)
    print(f"\nCollected {len(results)} articles")
