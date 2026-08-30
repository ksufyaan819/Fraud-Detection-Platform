import React from 'react';
import { SHAPFactor } from '../api/fraudApi';

interface Props {
  factors: SHAPFactor[];
}

export const FeatureImportanceBar: React.FC<Props> = ({ factors }) => {
  return (
    <div style={{ marginTop: '20px' }}>
      <h3 style={{ fontSize: '18px', marginBottom: '20px', color: '#1f2937' }}>
        XGBoost Decision Factors (SHAP)
      </h3>
      <div>
        {factors.map((factor) => {
          const isPositive = factor.contribution > 0;
          const barWidth = Math.min(Math.abs(factor.contribution) * 40, 100);
          
          return (
            <div key={factor.feature} className="shap-bar-container">
              <div className="shap-bar-labels">
                <span style={{ fontWeight: '500', color: '#4b5563' }}>{factor.feature}</span>
                <span style={{ color: isPositive ? '#ef4444' : '#22c55e', fontWeight: 'bold' }}>
                  {isPositive ? '+' : ''}{factor.contribution.toFixed(2)}
                </span>
              </div>
              <div className="shap-bar-wrapper">
                <div className="shap-bar-left" style={{ paddingRight: '2px' }}>
                  {!isPositive && (
                    <div className="shap-bar-fill" style={{ width: `${barWidth}%`, backgroundColor: '#4ade80' }} />
                  )}
                </div>
                <div className="shap-bar-right" style={{ paddingLeft: '2px' }}>
                  {isPositive && (
                    <div className="shap-bar-fill" style={{ width: `${barWidth}%`, backgroundColor: '#f87171' }} />
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};