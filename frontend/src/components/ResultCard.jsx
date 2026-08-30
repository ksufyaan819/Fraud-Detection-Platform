export default function ResultCard({ result, error }) {
  if (error) {
    return (
      <div className="result-card error">
        <h3>Error</h3>
        <p>{error.message || "An error occurred connecting to the backend."}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="result-card empty">
        <p>Submit a transaction to see the fraud prediction.</p>
      </div>
    );
  }

  // Assuming your XGBoost backend returns something like { fraud: boolean, risk_score: float }
  // Adjust these keys based on your actual FastApi JSON response
  const isFraud = result.fraud || result.prediction === 1;
  const confidence = result.risk_score || result.probability || 0;

  return (
    <div className={`result-card ${isFraud ? 'fraud' : 'safe'}`}>
      <h3>Prediction Result</h3>
      <div className="status-badge">
        {isFraud ? '🚨 FRAUD DETECTED' : '✅ SAFE TRANSACTION'}
      </div>
      <div className="details">
        <p><strong>Transaction ID:</strong> {result.transaction_id || 'N/A'}</p>
        <p><strong>Risk Score:</strong> {(confidence * 100).toFixed(2)}%</p>
      </div>
      <pre className="raw-json">{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}