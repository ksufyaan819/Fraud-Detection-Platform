import { useState } from 'react';

export default function TransactionForm({ onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    transaction_id: `TXN-${Math.floor(Math.random() * 100000)}`,
    amount: 150.50,
    merchant_category: 'retail',
    distance_from_home: 12.5,
    distance_from_last_transaction: 3.2,
    ratio_to_median_purchase_price: 1.1,
    used_chip: 1,
    used_pin_number: 0,
    online_order: 1
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Cast to exact schema types required by FastAPI
    const payload = {
      transaction_id: formData.transaction_id,
      amount: parseFloat(formData.amount),
      merchant_category: formData.merchant_category,
      distance_from_home: parseFloat(formData.distance_from_home),
      distance_from_last_transaction: parseFloat(formData.distance_from_last_transaction),
      ratio_to_median_purchase_price: parseFloat(formData.ratio_to_median_purchase_price),
      used_chip: parseInt(formData.used_chip, 10),
      used_pin_number: parseInt(formData.used_pin_number, 10),
      online_order: parseInt(formData.online_order, 10),
    };

    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h3>Transaction Details</h3>
      
      <div className="form-grid">
        <div className="input-group">
          <label>Transaction ID</label>
          <input type="text" name="transaction_id" value={formData.transaction_id} onChange={handleChange} required />
        </div>
        
        <div className="input-group">
          <label>Amount ($)</label>
          <input type="number" step="0.01" name="amount" value={formData.amount} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Merchant Category</label>
          <select name="merchant_category" value={formData.merchant_category} onChange={handleChange}>
            <option value="retail">Retail</option>
            <option value="travel">Travel</option>
            <option value="food">Food</option>
            <option value="entertainment">Entertainment</option>
          </select>
        </div>

        <div className="input-group">
          <label>Distance From Home</label>
          <input type="number" step="0.01" name="distance_from_home" value={formData.distance_from_home} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Distance From Last Txn</label>
          <input type="number" step="0.01" name="distance_from_last_transaction" value={formData.distance_from_last_transaction} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Ratio to Median Price</label>
          <input type="number" step="0.01" name="ratio_to_median_purchase_price" value={formData.ratio_to_median_purchase_price} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Used Chip (1=Yes, 0=No)</label>
          <input type="number" min="0" max="1" name="used_chip" value={formData.used_chip} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Used PIN (1=Yes, 0=No)</label>
          <input type="number" min="0" max="1" name="used_pin_number" value={formData.used_pin_number} onChange={handleChange} required />
        </div>

        <div className="input-group">
          <label>Online Order (1=Yes, 0=No)</label>
          <input type="number" min="0" max="1" name="online_order" value={formData.online_order} onChange={handleChange} required />
        </div>
      </div>

      <button type="submit" disabled={isLoading} className="submit-btn">
        {isLoading ? 'Scoring...' : 'Run Fraud Check'}
      </button>
    </form>
  );
}