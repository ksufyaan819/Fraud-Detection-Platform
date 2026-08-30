import { useState } from 'react';
import TransactionForm from './components/TransactionForm';
import ResultCard from './components/ResultCard';
import Dashboard from './components/Dashboard'; 
import { InvestigationDashboard } from './components/InvestigationDashboard';
import { scoreTransaction } from './services/api';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleScoreTransaction = async (payload) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const data = await scoreTransaction(payload);
      setResult(data);
    } catch (err) {
      setError(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Fraud Detection Platform</h1>
        <p>XGBoost ML Pipeline - Model Interface & Live Monitoring</p>
      </header>
      
      <main>
        {/* SECTION 1: Manual Transaction Scoring */}
        <section className="manual-section">
          <h2 style={{ marginBottom: '1rem', color: '#1f2937' }}>Manual Transaction Testing</h2>
          <div className="dashboard-grid">
            <div className="input-section">
              <TransactionForm onSubmit={handleScoreTransaction} isLoading={isLoading} />
            </div>
            
            <div className="result-section">
              <ResultCard result={result} error={error} />
            </div>
          </div>
        </section>

        <hr className="section-divider" />

        {/* SECTION 2: Live Monitoring Dashboard */}
        <section className="monitoring-section">
          <h2 style={{ marginBottom: '1rem', color: '#1f2937' }}>Live Traffic Monitoring</h2>
          <Dashboard />
        </section>

        <hr className="section-divider" />

        {/* SECTION 3: Fraud Investigation & Explainability (Part 6) */}
        <section className="investigation-section">
          <h2 style={{ marginBottom: '1rem', color: '#1f2937', paddingLeft: '1.5rem' }}>
            Fraud Investigation & Model Explainability
          </h2>
          <InvestigationDashboard />
        </section>
      </main>
    </div>
  );
}

export default App;