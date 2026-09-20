export function App() {
  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <header>
        <h1>MicroBots Control Dashboard</h1>
        <p style={{ color: '#666' }}>
          Open-source persistent AI worker platform (Baseline Recovery Mode)
        </p>
      </header>

      <section style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #e2e8f0', borderRadius: '8px' }}>
        <h2>System Baseline Status</h2>
        <ul>
          <li><strong>Backend API</strong>: FastAPI / oap package namespace</li>
          <li><strong>Protocol</strong>: @microbots/protocol shared types</li>
          <li><strong>Unit Test Status</strong>: 153/153 Python unit tests passing</li>
          <li><strong>Client Status</strong>: Baseline React / Vite Application Shell</li>
        </ul>
      </section>

      <section style={{ marginTop: '2rem', padding: '1rem', background: '#f8fafc', borderRadius: '8px' }}>
        <h3>Milestone Roadmap</h3>
        <p>Full API endpoints and worker integrations will become active as milestone release gates are reached.</p>
      </section>
    </main>
  );
}
