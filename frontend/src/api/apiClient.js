// fraud_platform/frontend/src/api/apiClient.js

// Ensure your FastAPI backend URL is set in your .env or defaults to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const getFraudStats = async () => {
  const response = await fetch(`${API_BASE_URL}/stats`);
  if (!response.ok) {
    throw new Error('Failed to fetch fraud statistics');
  }
  return response.json();
};

export const getRecentTransactions = async () => {
  const response = await fetch(`${API_BASE_URL}/transactions/recent`);
  if (!response.ok) {
    throw new Error('Failed to fetch recent transactions');
  }
  return response.json();
};

export const predictTransaction = async (transactionData) => {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(transactionData),
  });
  if (!response.ok) {
    throw new Error('Failed to run XGBoost prediction');
  }
  return response.json();
};