const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface FlaggedTransaction {
  id: string;
  amount: number;
  score: number;
}

export interface SHAPFactor {
  feature: string;
  contribution: number;
}

export interface ExplanationResult {
  transaction_id: string;
  fraud_score: number;
  factors: SHAPFactor[];
}

export const fetchFlaggedTransactions = async (): Promise<FlaggedTransaction[]> => {
  const response = await fetch(`${API_BASE_URL}/investigate`);
  if (!response.ok) throw new Error('Failed to fetch flagged transactions');
  return response.json();
};

export const fetchTransactionExplanation = async (txId: string): Promise<ExplanationResult> => {
  const response = await fetch(`${API_BASE_URL}/explain/${txId}`);
  if (!response.ok) throw new Error('Failed to fetch explanation');
  return response.json();
};