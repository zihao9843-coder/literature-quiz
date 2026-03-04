import { loadQuestions } from '../../lib/questions';

export default function QuizPage({ searchParams }: { searchParams: Record<string, string> }) {
  const questions = loadQuestions();
  const periods = [...new Set(questions.map((q) => q['时期']))];
  const kps = [...new Set(questions.map((q) => q['知识点']))];
  const types = [...new Set(questions.map((q) => q['题型']))];
  const levels = [...new Set(questions.map((q) => q['难度']))];

  const filtered = questions.filter((q) =>
    (!searchParams.period || q['时期'] === searchParams.period) &&
    (!searchParams.kp || q['知识点'] === searchParams.kp) &&
    (!searchParams.type || q['题型'] === searchParams.type) &&
    (!searchParams.level || q['难度'] === searchParams.level)
  );

  return (
    <main>
      <h2>/quiz 刷题</h2>
      <p>支持按时期、知识点、题型、难度筛选。</p>
      <form style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8 }}>
        <select name="period" defaultValue={searchParams.period || ''}><option value="">全部时期</option>{periods.map((x)=><option key={x}>{x}</option>)}</select>
        <select name="kp" defaultValue={searchParams.kp || ''}><option value="">全部知识点</option>{kps.slice(0,100).map((x)=><option key={x}>{x}</option>)}</select>
        <select name="type" defaultValue={searchParams.type || ''}><option value="">全部题型</option>{types.map((x)=><option key={x}>{x}</option>)}</select>
        <select name="level" defaultValue={searchParams.level || ''}><option value="">全部难度</option>{levels.map((x)=><option key={x}>{x}</option>)}</select>
        <button type="submit">筛选</button>
      </form>
      <p>当前题量：{filtered.length}</p>
      <ol>
        {filtered.slice(0, 20).map((q, i) => (
          <li key={i}><b>{q['题目']}</b>（{q['题型']} / {q['时期']}）</li>
        ))}
      </ol>
    </main>
  );
}
