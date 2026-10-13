import React from 'react';

const FraudAlertsTable = ({ transactions }) => {
  if (!transactions || transactions.length === 0) {
    return <div style={{ padding: '2rem', textAlign: 'center', color: '#6b7280' }}>No recent transactions available.</div>;
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #e5e7eb', color: '#6b7280', fontSize: '0.875rem' }}>
            <th style={{ padding: '1rem' }}>TRANSACTION ID</th>
            <th style={{ padding: '1rem' }}>TIMESTAMP</th>
            <th style={{ padding: '1rem' }}>AMOUNT</th>
            <th style={{ padding: '1rem' }}>XGBOOST RISK SCORE</th>
            <th style={{ padding: '1rem' }}>STATUS</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => {
            // Determine if it should be marked as fraud based on the backend data
            const isFraud = tx.prediction === 'fraud' || tx.status === 'Fraud' || tx.score > 0.70;
            
            return (
              <tr key={tx.id} style={{ borderBottom: '1px solid #f3f4f6' }}>
                <td style={{ padding: '1rem', fontWeight: 'bold' }}>#{tx.id}</td>
                <td style={{ padding: '1rem', color: '#4b5563' }}>{new Date(tx.timestamp).toLocaleString()}</td>
                <td style={{ padding: '1rem', color: '#4b5563' }}>${tx.amount.toFixed(2)}</td>
                <td style={{ padding: '1rem', fontWeight: 'bold' }}>
                  {tx.riskScore !== undefined ? tx.riskScore : Math.round(tx.score * 100)}%
                </td>
                <td style={{ padding: '1rem' }}>
                  {isFraud ? (
                    <span style={{ 
                      color: '#dc2626', 
                      backgroundColor: '#fee2e2', 
                      padding: '0.25rem 0.75rem', 
                      borderRadius: '9999px', 
                      fontWeight: 'bold',
                      fontSize: '0.875rem'
                    }}>
                      Fraud
                    </span>
                  ) : (
                    <span style={{ 
                      color: '#16a34a', 
                      backgroundColor: '#dcfce7', 
                      padding: '0.25rem 0.75rem', 
                      borderRadius: '9999px', 
                      fontWeight: 'bold',
                      fontSize: '0.875rem'
                    }}>
                      Clean
                    </span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default FraudAlertsTable;