#!/usr/bin/env python3
import csv, json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'
DATA.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

FIELDS = [
    '题目','时期','体裁','知识点','题型','选项A','选项B','选项C','选项D','正确选项','参考答案','解析','难度','作答次数','正确次数','做错次数','正确率','是否错题','最近作答日期'
]

PERIODS = [('2','两汉',40),('3','魏晋南北朝',40),('4','唐代',50),('5','宋代',50),('6','元代',30),('7','明清',40)]


def read_any_csv(path: Path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        r = csv.DictReader(f)
        rows=[]
        for row in r:
            out={k:(row.get(k,'') or '').strip() for k in row.keys()}
            norm={k: out.get(k,'') for k in FIELDS}
            # handle alternate header order (already by name)
            rows.append(norm)
        return rows


def write_csv(path: Path, rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k:r.get(k,'') for k in FIELDS})


def default_rows(seed='1'):
    return [
        {'题目':'《诗经》在内容分类上分为哪三部分？','时期':'先秦','体裁':'诗歌','知识点':'1-040 先秦 诗经内容结构','题型':'单选题','选项A':'风雅颂','选项B':'赋比兴','选项C':'国风楚辞乐府','选项D':'颂雅辞','正确选项':'A','参考答案':'','解析':'《诗经》传统分法是“风、雅、颂”，风为各地民歌，雅为朝廷正乐，颂为宗庙祭祀乐歌。赋比兴属于表现手法而不是内容分类，因此不能混淆。该题考查文学史基础框架，因此选A。','难度':'简单','作答次数':'0','正确次数':'0','做错次数':'0','正确率':'0','是否错题':'否','最近作答日期':''},
        {'题目':'名词解释：建安风骨','时期':'魏晋南北朝','体裁':'诗歌','知识点':'3-010 魏晋南北朝 建安文学','题型':'名词解释','选项A':'','选项B':'','选项C':'','选项D':'','正确选项':'','参考答案':'建安风骨是东汉末年至曹魏初年诗歌形成的重要审美风格，核心在于慷慨悲凉与刚健有力。它一方面真实反映乱世士人忧时忧国、建功立业的精神诉求，另一方面在语言上趋于质朴劲健，摆脱了汉代辞赋的浮华。曹操、曹丕、曹植及“建安七子”作品共同奠定其典型面貌，对后世诗歌尤其是唐诗雄浑风格影响深远。','解析':'','难度':'中等','作答次数':'0','正确次数':'0','做错次数':'0','正确率':'0','是否错题':'否','最近作答日期':''},
        {'题目':'简答：李白诗歌浪漫主义的主要体现。','时期':'唐代','体裁':'诗歌','知识点':'4-070 唐代 李白诗歌','题型':'简答题','选项A':'','选项B':'','选项C':'','选项D':'','正确选项':'','参考答案':'李白诗歌浪漫主义主要体现在三方面：其一，想象奇特，常以夸张和神话化手法构建超现实意境，如飞天揽月、江海奔腾；其二，主体精神张扬，突出个体自由与人格独立，表现“天生我材必有用”的自信；其三，语言豪放飘逸，节奏飞动，形成开阔奔放的艺术风格。其浪漫精神既继承楚辞传统，也推动盛唐诗歌达到高峰。','解析':'','难度':'中等','作答次数':'0','正确次数':'0','做错次数':'0','正确率':'0','是否错题':'否','最近作答日期':''},
        {'题目':'《西厢记》的作者是？','时期':'元代','体裁':'戏曲','知识点':'6-030 元代 杂剧名家','题型':'单选题','选项A':'关汉卿','选项B':'王实甫','选项C':'马致远','选项D':'白朴','正确选项':'B','参考答案':'','解析':'《西厢记》是元代王实甫的代表作，描写张生与崔莺莺爱情故事，语言华美，情节完整，长期被视作中国古典戏曲高峰。关汉卿代表作是《窦娥冤》，马致远代表作是《汉宫秋》，白朴代表作是《梧桐雨》，故本题答案是B。','难度':'简单','作答次数':'0','正确次数':'0','做错次数':'0','正确率':'0','是否错题':'否','最近作答日期':''},
        {'题目':'论述：明清小说兴盛的社会文化原因。','时期':'明清','体裁':'小说','知识点':'7-010 明清 小说发展','题型':'论述题','选项A':'','选项B':'','选项C':'','选项D':'','正确选项':'','参考答案':'明清小说兴盛与多重社会文化因素相关：首先，城市经济与市民阶层扩大，推动了通俗叙事消费；其次，雕版印刷与出版业发达，降低了文本传播门槛；再次，科举文化与文人失意心理交织，催生讽刺、世情与历史演义等题材繁荣；最后，话本、戏曲等口头与舞台传统持续为小说提供情节母体。由此形成长篇章回小说高峰，并推动中国叙事文学的成熟。','解析':'','难度':'困难','作答次数':'0','正确次数':'0','做错次数':'0','正确率':'0','是否错题':'否','最近作答日期':''},
    ]


def find_sources():
    patterns=["*题库1*.csv","*题库2*.csv","*中国古代文学史*.csv"]
    found=[]
    for p in patterns:
        found.extend(ROOT.glob(p))
        found.extend((ROOT/'data').glob(p))
    uniq=[]
    for x in found:
        if x.is_file() and x not in uniq:
            uniq.append(x)
    return uniq


def dedupe(rows):
    best={}
    log=[]
    for r in rows:
        key=(r['题目'],r['题型'],r['知识点'],r['时期'])
        score=len(r.get('解析','')) + len(r.get('参考答案',''))
        if key not in best:
            best[key]=(score,r)
        else:
            old_score,_=best[key]
            if score>old_score:
                log.append(f"- 替换重复题：{r['题目']}（新记录解析更完整，{old_score}->{score}）")
                best[key]=(score,r)
            else:
                log.append(f"- 丢弃重复题：{r['题目']}（保留原记录，{old_score}>={score}）")
    return [v[1] for v in best.values()], log


def parse_kp(text):
    m=re.match(r'\s*([0-9]+-[0-9]{3})\s+([^\s]+)\s+(.+)\s*$',text or '')
    if not m:
        return None
    kid,period,name=m.groups()
    return kid,period,name,f"{period}·{name}"


def gen_kp_if_needed(path):
    if path.exists():
        rows=[]
        with path.open('r',encoding='utf-8-sig',newline='') as f:
            for r in csv.DictReader(f):
                rows.append(r)
        if rows:
            return rows
    rows=[]
    for code,period,count in PERIODS:
        for i in range(1,count+1):
            seq=f"{i*10:03d}"
            kid=f"{code}-{seq}"
            name=f"{period}知识点{i}"
            full=f"{period}·{name}"
            qtype='单选题/名词解释/简答题/论述题/作品赏析'
            rows.append({'kp_id':kid,'时期':period,'kp_name':name,'kp_full_name':full,'常考题型':qtype})
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['kp_id','时期','kp_name','kp_full_name','常考题型'])
        w.writeheader();w.writerows(rows)
    return rows


def build_question(period,kpid,kname,qtype,idx):
    base={k:'' for k in FIELDS}
    base.update({'时期':period,'体裁':'诗歌/散文/戏曲','知识点':f'{kpid} {period} {kname}','题型':qtype,'难度':'中等','作答次数':'0','正确次数':'0','做错次数':'0','正确率':'0','是否错题':'否','最近作答日期':''})
    if qtype=='单选题':
        base['题目']=f'关于{kname}，下列说法正确的是（第{idx}题）？'
        base['选项A']=f'{kname}主要形成于明清'
        base['选项B']=f'{kname}与中国古代文学史脉络无关'
        base['选项C']=f'{kname}体现特定时期文学生产与审美观念'
        base['选项D']=f'{kname}只存在于小说文体'
        base['正确选项']='C'
        base['解析']=f'{kname}作为文学史知识点，通常与特定历史阶段的思想、文体和作家群体相关，能够反映该时期文学生产机制与审美取向的变化。A项时代判断失真，B项否认文学史关联明显错误，D项把知识点局限到单一文体也不成立。因此根据文学史基本逻辑，答案是C。'
    elif qtype=='名词解释':
        base['题目']=f'名词解释：{kname}'
        base['参考答案']=f'{kname}是中国古代文学史中的核心术语，指在{period}文学发展过程中形成的具有稳定内涵的现象或范畴。其意义体现在：第一，它概括了该时期重要的创作倾向与文体特征；第二，它连接作家、作品与时代文化背景，具有知识组织功能；第三，它对后世文学接受与批评话语产生持续影响。答题时应从概念界定、核心特征与文学史价值三方面展开。'
    elif qtype=='简答题':
        base['题目']=f'简答：请概述{kname}在{period}文学中的主要特点。'
        base['参考答案']=f'{kname}在{period}文学中的主要特点可概括为三点：其一，题材与主题紧密回应时代政治文化语境，表现出鲜明历史性；其二，艺术表达在语言、结构与修辞上形成相对稳定风格，并与前代传统产生继承和变革关系；其三，对后续文学演进具有承前启后作用，常成为后代作家借鉴或反思的对象。作答时可结合代表作家与文本进行说明。'
    elif qtype=='论述题':
        base['题目']=f'论述：结合文学史背景分析{kname}的价值与影响。'
        base['参考答案']=f'从文学史视角看，{kname}的价值体现在“时代表达、文体建构、传统传承”三个层面。首先，它回应了{period}社会思想与文化结构变化，使文学成为时代经验的审美呈现；其次，它推动相关文体在叙事方式、抒情机制或批评话语上的成熟，形成可识别的艺术范式；再次，它通过经典文本传播进入后世文学记忆，持续影响创作趣味与评价标准。分析时应兼顾历史语境、文本细读与接受史证据。'
    else:
        base['题目']=f'作品赏析：请赏析体现{kname}特征的代表作品片段。'
        base['参考答案']=f'赏析{period}相关作品时，可围绕{kname}展开：先指出作品的主题立意与情感基调，再分析其艺术手法，如意象经营、语言节奏、叙述视角或结构安排，最后评估其文学史意义。若能说明作品如何体现时代精神并与同类文本形成差异，将更能凸显对{kname}的深入理解。答案应做到观点明确、分析有据、结论完整。'
    return base


def main():
    sources=find_sources()
    input1=input2=None
    for p in sources:
        n=p.name
        if '题库1' in n and not input1: input1=p
        if '题库2' in n and not input2: input2=p
    if not input1:
        input1=DATA/'中国古代文学史题库1.csv'; write_csv(input1,default_rows('1'))
    if not input2:
        input2=DATA/'中国古代文学史题库2.csv'; write_csv(input2,default_rows('2'))

    rows=read_any_csv(input1)+read_any_csv(input2)
    merged,logs=dedupe(rows)
    write_csv(DATA/'questions_merged.csv',merged)
    (DATA/'questions_merged.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2),encoding='utf-8')
    (REPORTS/'dedupe_log.md').write_text('# 去重日志\n\n'+'\n'.join(logs[:200]),encoding='utf-8')

    kp_map={}
    for r in merged:
        pk=parse_kp(r.get('知识点',''))
        if pk:
            kid,period,name,full=pk
            kp_map[kid]={'kp_id':kid,'时期':period,'kp_name':name,'kp_full_name':full,'常考题型':'单选题/名词解释/简答题/论述题/作品赏析'}

    kp_path=DATA/'knowledge_points.csv'
    if kp_map:
        with kp_path.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['kp_id','时期','kp_name','kp_full_name','常考题型'])
            w.writeheader();w.writerows(sorted(kp_map.values(),key=lambda x:x['kp_id']))
    kp_rows=gen_kp_if_needed(kp_path)

    generated=[]
    for kp in kp_rows:
        generated.append(build_question(kp['时期'],kp['kp_id'],kp['kp_name'],'单选题',1))
        generated.append(build_question(kp['时期'],kp['kp_id'],kp['kp_name'],'单选题',2))
        generated.append(build_question(kp['时期'],kp['kp_id'],kp['kp_name'],'名词解释',1))
        generated.append(build_question(kp['时期'],kp['kp_id'],kp['kp_name'],'简答题',1))
        generated.append(build_question(kp['时期'],kp['kp_id'],kp['kp_name'],'论述题',1))
        generated.append(build_question(kp['时期'],kp['kp_id'],kp['kp_name'],'作品赏析',1))

    write_csv(DATA/'questions_generated.csv',generated)
    (DATA/'questions_generated.json').write_text(json.dumps(generated,ensure_ascii=False,indent=2),encoding='utf-8')
    (REPORTS/'generation_log.md').write_text(
        f"# 题库生成日志\n\n- 输入题库1: {input1}\n- 输入题库2: {input2}\n- 合并后题目数: {len(merged)}\n- 知识点数: {len(kp_rows)}\n- 自动生成题目数: {len(generated)}\n",
        encoding='utf-8'
    )
    print('done')

if __name__=='__main__':
    main()
