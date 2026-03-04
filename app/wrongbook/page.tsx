import { loadWrongQuestions } from '../../lib/questions';

export default function WrongBookPage() {
  const list = loadWrongQuestions();
  return (
    <main>
      <h2>/wrongbook 错题本</h2>
      <a href="/wrongbook/print">一键打印页面</a>
      <p>错题数量：{list.length}</p>
      <ol>
        {list.slice(0, 50).map((q, i) => <li key={i}>{q['题目']}（{q['题型']}）</li>)}
      </ol>
    </main>
  );
}
