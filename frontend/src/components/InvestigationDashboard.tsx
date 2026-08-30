import React, { useEffect, useState } from 'react';
import { fetchFlaggedTransactions, fetchTransactionExplanation } from '../services/api';
import { FeatureImportanceBar } from './FeatureImportanceBar';

export const InvestigationDashboard = () => {
  // TypeScript types added to prevent 'never[]' and missing variable errors
  const [queue, setQueue] = useState<any[]>([]);
  const [selectedTx, setSelectedTx] = useState<string | null>(null);
  const [explanation, setExplanation] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const loadQueue = async () => {
      try {
        const data = await fetchFlaggedTransactions();
        setQueue(data);
      } catch (error) {
        console.error("Failed to load queue:", error);
      }
    };
    loadQueue();
  }, []);

  useEffect(() => {
    if (!selectedTx) return;
    
    const loadExplanation = async () => {
      setLoading(true);
      try {
        const data = await fetchTransactionExplanation(selectedTx);
        setExplanation(data);
      } catch (error) {
        console.error("Failed to load explanation:", error);
      } finally {
        setLoading(false);
      }
    };
    loadExplanation();
  }, [selectedTx]);

  return (
    <div className="investigation-container">
      {/* Left Column: Flagged Queue */}
      <div className="queue-panel">
        <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: '#1f2937' }}>Investigation Queue</h2>
        <div>
          {queue.length === 0 ? <p style={{color: '#6b7280'}}>No flagged transactions.</p> : null}
          {queue.map((tx) => (
            <button
              key={tx.id}
              onClick={() => setSelectedTx(tx.id)}
              className={`queue-button ${selectedTx === tx.id ? 'active' : ''}`}
            >
              <div className="queue-id">{tx.id}</div>
              <div className="queue-details">
                <span style={{ color: '#6b7280' }}>${tx.amount.toFixed(2)}</span>
                <span style={{ color: '#dc2626', fontWeight: 'bold' }}>
                  {(tx.score * 100).toFixed(1)}% Risk
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Right Column: Explanation View */}
      <div className="details-panel">
        {selectedTx ? (
          <div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#1f2937' }}>
              Transaction: {selectedTx}
            </h2>
            {loading ? (
              <p style={{ color: '#6b7280' }}>Running explainer...</p>
            ) : explanation ? (
              <>
                <div style={{ marginBottom: '1.5rem' }}>
                  <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>
                    Model Confidence
                  </span>
                  <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc2626' }}>
                    {(explanation.fraud_score * 100).toFixed(2)}%
                  </div>
                </div>
                <FeatureImportanceBar factors={explanation.factors} />
              </>
            ) : null}
          </div>
        ) : (
          <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center', color: '#6b7280', border: '2px dashed #e5e7eb', borderRadius: '8px' }}>
            Select a transaction from the queue to investigate.
          </div>
        )}
      </div>
    </div>
  );
};