import React, { useState, useEffect } from 'react';
import StatCard from './StatCard';
import FraudAlertsTable from './FraudAlertsTable';
import { getFraudStats, getRecentTransactions } from '../api/apiClient';

const Dashboard = () => {
  // 1. Updated the initial state to look for xgboostAccuracy instead of modelAccuracy
  const [stats, setStats] = useState({ totalScanned: 0, fraudCaught: 0, xgboostAccuracy: 0 });
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboardData = async () => {
    try {
      const [statsData, txData] = await Promise.all([
        getFraudStats(),
        getRecentTransactions()
      ]);
      setStats(statsData);
      setTransactions(txData);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Failed to sync with FastAPI backend. Ensure the server is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
    const intervalId = setInterval(loadDashboardData, 10000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading && transactions.length === 0) {
    return <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem' }}>Loading ML Platform...</div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Fraud Detection Command Center</h1>
        <p>Live transaction monitoring powered by FastAPI & XGBoost</p>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="stats-grid">
        <StatCard 
          title="Total Transactions Scanned" 
          value={stats.totalScanned} 
          colorClass="border-blue" 
        />
        <StatCard 
          title="Fraudulent Activity Caught" 
          value={stats.fraudCaught} 
          colorClass="border-red" 
        />
        <StatCard 
          title="XGBoost Accuracy" 
          // 2. Updated to read xgboostAccuracy and dynamically append the '%' symbol!
          value={`${stats.xgboostAccuracy || 0}%`} 
          colorClass="border-green" 
        />
      </div>

      <div>
        <div className="table-section-header">
          <h2>Recent API Predictions</h2>
          <button onClick={loadDashboardData} className="refresh-button">
            Force Refresh Data
          </button>
        </div>
        <FraudAlertsTable transactions={transactions} />
      </div>
    </div>
  );
};

export default Dashboard;