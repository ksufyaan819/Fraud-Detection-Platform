import React from 'react';

const FraudAlertsTable = ({ transactions }) => {
  if (!transactions || transactions.length === 0) {
    return <div style={{ padding: '1rem', textAlign: 'center', color: '#6b7280' }}>No transactions available.</div>;
  }

  return (
    <div className="table-container">
      <table className="alerts-table">
        <thead>
          <tr>
            <th>Transaction ID</th>
            <th>Timestamp</th>
            <th>Amount</th>
            <th>XGBoost Risk Score</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => (
            <tr key={tx.id}>
              <td style={{ fontWeight: 'bold', color: '#111827' }}>#{tx.id}</td>
              <td>{new Date(tx.timestamp).toLocaleString()}</td>
              <td>${tx.amount.toFixed(2)}</td>
              <td style={{ fontWeight: 'bold' }}>{tx.riskScore}%</td>
              <td>
                <span className={`status-badge ${tx.isFraud ? 'status-fraud' : 'status-clean'}`}>
                  {tx.isFraud ? 'Fraud Detected' : 'Clean'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FraudAlertsTable;