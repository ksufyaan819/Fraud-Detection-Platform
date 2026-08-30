import React from 'react';

const StatCard = ({ title, value, colorClass }) => {
  return (
    <div className={`stat-card ${colorClass}`}>
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
};

export default StatCard;