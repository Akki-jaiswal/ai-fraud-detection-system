import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeText = async () => {
    if (!text) return;
    setLoading(true);
    setError(null);

    try {
      // This connects your React frontend to your Python FastAPI backend
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
      });

      if (!response.ok) throw new Error('Analysis failed');
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Could not connect to the AI model. Is the FastAPI server running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🛡️ Fraud Detection AI</h1>
        <p>Real-time threat analysis powered by Ensemble ML</p>
      </header>

      <div className="analyzer-box">
        <textarea 
          placeholder="Paste a suspicious message, email, or call transcript here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
        />
        <button onClick={analyzeText} disabled={loading || !text}>
          {loading ? 'Analyzing...' : 'Scan for Fraud'}
        </button>
      </div>

      {error && <div className="error-box">{error}</div>}

      {result && (
        <div className="results-card">
          <h2>Analysis Complete</h2>
          
          <div className="metrics">
            <div className={`metric-box risk-${result.risk_level.toLowerCase()}`}>
              <span className="label">Risk Level</span>
              <span className="value">{result.risk_level}</span>
            </div>
            
            <div className="metric-box">
              <span className="label">Threat Score</span>
              <span className="value">{result.risk_score} / 100</span>
            </div>
            
            <div className={`metric-box ${result.is_fraud ? 'fraud-alert' : 'safe'}`}>
              <span className="label">Verdict</span>
              <span className="value">{result.is_fraud ? 'FRAUD DETECTED' : 'NORMAL'}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App