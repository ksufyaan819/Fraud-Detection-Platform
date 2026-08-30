import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const scoreTransaction = async (transactionData) => {
  try {
    // Fixed endpoint to match your main.py (/api/score instead of /api/v1/score)
    const response = await axios.post(`${API_BASE_URL}/api/score`, transactionData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    throw error.response?.data || new Error("Failed to connect to the backend");
  }
};

// NEW: Fetch flagged transactions for the queue
export const fetchFlaggedTransactions = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/investigate`);
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    throw error.response?.data || new Error("Failed to fetch investigation queue");
  }
};

// NEW: Fetch SHAP explanation for a specific transaction
export const fetchTransactionExplanation = async (transactionId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/explain/${transactionId}`);
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    throw error.response?.data || new Error(`Failed to explain transaction ${transactionId}`);
  }
};