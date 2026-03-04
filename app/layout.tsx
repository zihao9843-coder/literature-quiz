export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body style={{ fontFamily: 'sans-serif', maxWidth: 1100, margin: '0 auto', padding: 24 }}>
        <h1>中国古代文学史刷题网站</h1>
        <nav style={{ display: 'flex', gap: 16, marginBottom: 20 }}>
          <a href="/quiz">刷题</a>
          <a href="/dashboard">学习统计</a>
          <a href="/wrongbook">错题本</a>
        </nav>
        {children}
      </body>
    </html>
  );
}
