#!/usr/bin/env python3
import csv
from pathlib import Path
from difflib import SequenceMatcher

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT/'data'/'questions_generated.csv'
REPORT = ROOT/'reports'/'validate_report.md'
FIELDS=['题目','时期','体裁','知识点','题型','选项A','选项B','选项C','选项D','正确选项','参考答案','解析','难度','作答次数','正确次数','做错次数','正确率','是否错题','最近作答日期']

rows=[]
if FILE.exists():
    with FILE.open('r',encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))

issues=[]
if rows:
    if list(rows[0].keys())!=FIELDS:
        issues.append('字段顺序或字段名不符合19列规范。')

for i,r in enumerate(rows, start=2):
    t=r.get('题型','')
    if t=='单选题':
        for k in ['选项A','选项B','选项C','选项D','正确选项','解析']:
            if not (r.get(k,'') or '').strip():
                issues.append(f'L{i} 单选题缺少字段：{k}')
        if len((r.get('解析') or '').strip())<80:
            issues.append(f'L{i} 单选题解析不足80字')
        p=(r.get('解析') or '')
        if '答案是' not in p and '因此选' not in p:
            issues.append(f'L{i} 解析未明确指出正确答案')
    if t in ['名词解释','简答题','论述题','作品赏析']:
        ans=(r.get('参考答案') or '').strip()
        if not ans:
            issues.append(f'L{i} 主观题缺少参考答案')
        if ans and not (50<=len(ans)<=350):
            issues.append(f'L{i} 主观题参考答案长度不在50-350字')

# similarity check
sim_hits=[]
for i in range(len(rows)):
    qi=(rows[i].get('题目') or '').strip()
    if not qi: continue
    for j in range(i+1,len(rows)):
        qj=(rows[j].get('题目') or '').strip()
        s=SequenceMatcher(None,qi,qj).ratio()
        if s>0.92:
            sim_hits.append((i+2,j+2,s,qi[:40],qj[:40]))

content=['# 题库校验报告','',f'- 文件: {FILE}','- 结果: ' + ('通过' if not issues else '存在问题'),f'- 总题数: {len(rows)}','', '## 问题明细']
if issues:
    content.extend([f'- {x}' for x in issues[:300]])
else:
    content.append('- 未发现字段完整性、题型规则或答案规则问题。')
content.extend(['','## 相似题检查（阈值>0.92）'])
if sim_hits:
    content.extend([f'- L{a} vs L{b} 相似度{s:.3f}: {x} / {y}' for a,b,s,x,y in sim_hits[:100]])
else:
    content.append('- 未发现高相似重复题。')
REPORT.write_text('\n'.join(content),encoding='utf-8')
print('issues',len(issues),'sim',len(sim_hits))
