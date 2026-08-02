
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

function App() {
  const [ticker, setTicker] = useState('RELIANCE');
  const [exchange, setExchange] = useState('NSE');
  const [stockData, setStockData] = useState(null);
  const [pipelineLog, setPipelineLog] = useState(null);
  const [loading, setLoading] = useState(false);
  const [serverWaking, setServerWaking] = useState(false);
  const [error, setError] = useState('');

  const [visibility, setVisibility] = useState({ open: true, close: true, high: false, low: false });

  const BACKEND_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const verifyServerState = async () => {
      try {
        const check = await fetch(`${BACKEND_URL}/api/health`);
        if (!check.ok) setServerWaking(true);
      } catch {
        setServerWaking(true);
      }
    };
    verifyServerState();
  }, [BACKEND_URL]);

  const fetchSnapshot = async () => {
    setLoading(true); 
    setError('');
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/stocks/snapshot/${exchange}/${ticker}`);
      if (!res.ok) throw new Error('Could not fetch data for this stock symbol.');
      const data = await res.json();
      setStockData(data);
      setServerWaking(false);
    } catch (err) {
      setError(err.message); 
      setStockData(null);
    } finally { 
      setLoading(false); 
    }
  };

  const triggerIngestionPipeline = async () => {
    setLoading(true); 
    setError(''); 
    setPipelineLog(null);
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/pipeline/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: ticker, exchange: exchange, s3_bucket: 'stock-sense-analytics-lake' })
      });
      if (!res.ok) throw new Error('The background data ingestion job failed.');
      const data = await res.json();
      setPipelineLog(data);
    } catch (err) {
      setError(err.message);
    } finally { 
      setLoading(false); 
    }
  };

  const toggleLine = (metric) => { 
    setVisibility((prev) => ({ ...prev, [metric]: !prev[metric] })); 
  };

  return (
    <div className="app-container">
      <header className="navbar">
        <h1>📊 Stock Sense Dashboard</h1>
        <span className="badge">Data Pipeline UI</span>
      </header>

      <main className="dashboard-grid">
        <section className="control-panel card">
          <h2>Controls</h2>
          <div className="input-group">
            <label>Ticker Symbol</label>
            <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value.toUpperCase())} />
          </div>

          <div className="input-group">
            <label>Exchange</label>
            <select value={exchange} onChange={(e) => setExchange(e.target.value)}>
              <option value="NSE">NSE</option>
              <option value="BSE">BSE</option>
            </select>
          </div>

          <div className="button-cluster">
            <button onClick={fetchSnapshot} disabled={loading} className="btn primary">View Chart</button>
            <button onClick={triggerIngestionPipeline} disabled={loading} className="btn secondary">Run Spark ETL</button>
          </div>

          {stockData?.historical_series?.length > 0 && (
            <div className="chart-toggles">
              <h3>Chart Filters</h3>
              <label><input type="checkbox" checked={visibility.open} onChange={() => toggleLine('open')} /> <span className="lbl-open">Open Price</span></label>
              <label><input type="checkbox" checked={visibility.close} onChange={() => toggleLine('close')} /> <span className="lbl-close">Close Price</span></label>
              <label><input type="checkbox" checked={visibility.high} onChange={() => toggleLine('high')} /> <span className="lbl-high">High</span></label>
              <label><input type="checkbox" checked={visibility.low} onChange={() => toggleLine('low')} /> <span className="lbl-low">Low</span></label>
            </div>
          )}
        </section>

        <section className="display-panel">
          {serverWaking && <div className="loader">Waking up remote server container, please wait...</div>}
          {loading && <div className="loader">Processing request...</div>}
          {error && <div className="banner error">⚠️ Error: {error}</div>}

          {stockData && (
            <div className="workspace-stack">
              <div className="card metrics-card">
                <h2>{stockData.company_name} ({stockData.ticker})</h2>
                <div className="metrics-grid">
                  <div className="metric-box"><small>Last Traded Price</small><p>₹{stockData.ltp}</p></div>
                  <div className="metric-box"><small>Market Cap</small><p>{stockData.market_cap_formatted}</p></div>
                </div>
              </div>

              {stockData.historical_series?.length > 0 && (
                <div className="card chart-card">
                  <h2>Historical Price (Past 30 Days)</h2>
                  <div style={{ width: '100%', height: 400 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={stockData.historical_series} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="date" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" domain={['auto', 'auto']} />
                        <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569', color: '#f8fafc' }} />
                        <Legend />
                        {visibility.open && <Line type="monotone" dataKey="open" stroke="#38bdf8" name="Open" strokeWidth={2} dot={{ r: 1 }} />}
                        {visibility.close && <Line type="monotone" dataKey="close" stroke="#4ade80" name="Close" strokeWidth={2} dot={{ r: 1 }} />}
                        {visibility.high && <Line type="monotone" dataKey="high" stroke="#f43f5e" name="High" strokeWidth={1.5} strokeDasharray="4 4" />}
                        {visibility.low && <Line type="monotone" dataKey="low" stroke="#fbbf24" name="Low" strokeWidth={1.5} strokeDasharray="4 4" />}
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}
            </div>
          )}

          {pipelineLog && (
            <div className="card log-card" style={{ marginTop: '2rem' }}>
              <h2>Pipeline Execution Logs</h2>
              <pre>{JSON.stringify(pipelineLog, null, 2)}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
