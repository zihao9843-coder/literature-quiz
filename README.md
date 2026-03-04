# 中国古代文学史刷题网站（literature-quiz）

本项目实现：
- 题库数据管理、自动生成、二次校验
- Next.js 刷题系统（`/quiz`）
- 学习进度统计（`/dashboard`）
- 错题本（`/wrongbook`）与一键打印（`/wrongbook/print`）
- SQLite + Prisma 数据层设计

## 目录结构

- `data/`：题库 CSV/JSON（合并与生成产物）
- `reports/`：去重、生成、校验报告
- `scripts/`：生成、校验、导入脚本
- `prisma/schema.prisma`：数据库结构
- `app/`：Next.js 页面

## 快速开始

```bash
pnpm install
pnpm dev
```

## 数据处理流程

1. 自动搜索题库文件：
   - `*题库1*.csv`
   - `*题库2*.csv`
   - `*中国古代文学史*.csv`
2. 若缺失则自动创建默认测试题库。
3. 合并为：
   - `data/questions_merged.csv`
   - `data/questions_merged.json`
4. 去重日志：`reports/dedupe_log.md`
5. 生成知识点：`data/knowledge_points.csv`
6. 自动出题：
   - `data/questions_generated.csv`
   - `data/questions_generated.json`
7. 校验报告：`reports/validate_report.md`

运行：

```bash
python scripts/generate_bank.py
python scripts/validate_bank.py
```

## 数据导入数据库

```bash
python scripts/import_csv_to_db.py
```

支持导入：
- `中国古代文学史题库1.csv`
- `中国古代文学史题库2.csv`
- `data/questions_merged.csv`

## 说明

- `dev.db` 为本地开发数据库文件，不应提交到仓库。
- 已在 `.gitignore` 中忽略 `prisma/dev.db`。
