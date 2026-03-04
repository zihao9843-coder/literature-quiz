#!/usr/bin/env python3
import csv, sqlite3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
DB=ROOT/'prisma'/'dev.db'

FILES=[
    ROOT/'中国古代文学史题库1.csv',
    ROOT/'中国古代文学史题库2.csv',
    DATA/'questions_merged.csv',
]

conn=sqlite3.connect(DB)
cur=conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Questions (
question_id INTEGER PRIMARY KEY AUTOINCREMENT,
题目 TEXT, 时期 TEXT, 体裁 TEXT, 知识点 TEXT, 题型 TEXT,
选项A TEXT, 选项B TEXT, 选项C TEXT, 选项D TEXT, 正确选项 TEXT,
参考答案 TEXT, 解析 TEXT, 难度 TEXT
)''')

inserted=0
for f in FILES:
    if not f.exists():
        continue
    with f.open('r',encoding='utf-8-sig',newline='') as fp:
        for row in csv.DictReader(fp):
            cur.execute('''INSERT INTO Questions (题目,时期,体裁,知识点,题型,选项A,选项B,选项C,选项D,正确选项,参考答案,解析,难度)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(
                            row.get('题目',''),row.get('时期',''),row.get('体裁',''),row.get('知识点',''),row.get('题型',''),
                            row.get('选项A',''),row.get('选项B',''),row.get('选项C',''),row.get('选项D',''),row.get('正确选项',''),
                            row.get('参考答案',''),row.get('解析',''),row.get('难度','')
                        ))
            inserted+=1
conn.commit(); conn.close()
print('imported',inserted,'to',DB)
