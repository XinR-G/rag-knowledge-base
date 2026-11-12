# RAG 知识库系统

## 问题
文档问答：上传文档，检索相关段落，生成带引用的回答。

## 方案
解析 → 切分 → 检索 → 重排 → 生成带引用回答。

## 架构图
（待补）

## 结果指标
（待补：基线 vs 优化后对比表）

## 怎么跑
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

