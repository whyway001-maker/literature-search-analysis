# 📚 文献自动检索下载分析

> 学术文献自动检索、批量下载与智能分析工具 —— 支持 CNKI（中国知网）、Google Scholar 等多源文献检索与下载，提供 AI 驱动的文献分析与综述生成。

## ✨ 功能特性

- **多源检索**：CNKI（中国知网）+ Google Scholar，关键词/高级/期刊检索
- **批量下载**：自动识别全文链接，批量下载 PDF/CAJ 文献
- **元数据导出**：导出结构化文献信息（BibTeX/CSV/JSON）
- **AI 分析**：文献摘要生成、知识图谱构建、主题聚类分析
- **引用分析**：引用链追踪、高被引文献筛选
- **阅读辅助**：PDF 解析、关键信息提取、综述生成

## 🏗️ 项目结构

```
文献自动检索下载分析/
├── src/
│   ├── search/          # 检索引擎（CNKI、Google Scholar）
│   ├── download/        # 下载管理器
│   ├── analysis/        # 文献分析（NLP、聚类、知识图谱）
│   └── utils/           # 工具函数（PDF解析、格式转换）
├── data/
│   ├── raw/             # 原始检索结果
│   └── processed/       # 清洗后数据
├── scripts/             # 自动化脚本
├── outputs/
│   ├── figures/         # 可视化图表
│   └── tables/          # 分析表格
├── paper/               # 论文稿件
├── tests/               # 测试用例
└── .github/workflows/   # CI/CD
```

## 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# CNKI 文献检索
python -m src.search.cnki "闭环供应链" --count 20

# Google Scholar 检索
python -m src.search.google_scholar "reverse logistics" --years 2020-2025

# 批量下载
python -m src.download.manager --source cnki --keywords "动力电池回收"

# 文献分析
python -m src.analysis.pipeline --input data/raw/results.json
```

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| 浏览器自动化 | Playwright / Chrome DevTools Protocol |
| 数据提取 | BeautifulSoup4, lxml |
| NLP 分析 | spaCy, jieba, scikit-learn |
| 知识图谱 | NetworkX |
| PDF 解析 | PyMuPDF, pdfplumber |
| 引用管理 | Zotero API |

## 📋 依赖技能（Codex Skills）

本项目依赖以下 Codex 技能模块，提供浏览器自动化与学术搜索能力：

- `cnki-search` — CNKI 基础检索
- `cnki-advanced-search` — CNKI 高级检索
- `cnki-download` — CNKI 文献下载
- `cnki-export` — CNKI 数据导出
- `cnki-paper-detail` — CNKI 论文详情
- `cnki-navigate-pages` — CNKI 页面翻页
- `cnki-journal-search` — CNKI 期刊检索
- `cnki-journal-toc` — CNKI 期刊目录
- `cnki-journal-index` — CNKI 期刊索引
- `gs-search` — Google Scholar 检索
- `gs-advanced-search` — Google Scholar 高级检索
- `gs-cited-by` — Google Scholar 引用追踪
- `gs-export` — Google Scholar 导出
- `gs-fulltext` — Google Scholar 全文获取
- `gs-navigate-pages` — Google Scholar 翻页
- `nature-*` — Nature 系列技能（学术写作/阅读/图表等）
- `PaperSpine` — 学术论文写作指导
- `zotero-mcp` — Zotero 文献管理集成

## 📄 License

MIT License
