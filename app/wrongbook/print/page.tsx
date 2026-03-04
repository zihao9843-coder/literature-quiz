import { loadWrongQuestions } from '../../../lib/questions';

export default function WrongBookPrintPage() {
  const list = loadWrongQuestions();
  return (
    <main>
      <h2>/wrongbook/print 错题打印</h2>
      <button type="button">导出 PDF（请使用浏览器打印另存为 PDF）</button>
      <hr />
      {list.map((q, i) => (
        <section key={i} style={{ marginBottom: 16 }}>
          <h4>{i + 1}. {q['题目']}</h4>
          <p>知识点：{q['知识点']}</p>
          <p>参考答案：{q['参考答案'] || q['解析']}</p>
        </section>
      ))}
    </main>
  );
}
