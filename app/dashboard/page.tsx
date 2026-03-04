import { loadQuestions } from '../../lib/questions';

export default function DashboardPage() {
  const questions = loadQuestions();
  const total = questions.length;
  const attempted = questions.filter((q) => Number(q['作答次数'] || 0) > 0).length;
  const correct = questions.reduce((s, q) => s + Number(q['正确次数'] || 0), 0);
  const wrong = questions.reduce((s, q) => s + Number(q['做错次数'] || 0), 0);
  const acc = correct + wrong > 0 ? ((correct / (correct + wrong)) * 100).toFixed(2) : '0';

  return (
    <main>
      <h2>/dashboard 学习进度统计</h2>
      <ul>
        <li>总题数：{total}</li>
        <li>已做题数：{attempted}</li>
        <li>正确率：{acc}%</li>
      </ul>
    </main>
  );
}
