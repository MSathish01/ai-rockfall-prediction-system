import React from 'react';
import { ProgressBar } from 'react-bootstrap';

const RiskGauge = ({ probability }) => {
  const percentage = Math.round(probability * 100);
  
  const getVariant = () => {
    if (percentage < 25) return 'success';
    if (percentage < 50) return 'warning';
    if (percentage < 75) return 'danger';
    return 'dark';
  };

  return (
    <div className="text-center">
      <div className="mb-2">
        <h3 className="mb-0">{percentage}%</h3>
        <small className="text-muted">Rockfall Probability</small>
      </div>
      <ProgressBar 
        now={percentage} 
        variant={getVariant()}
        style={{ height: '20px' }}
        label={`${percentage}%`}
      />
    </div>
  );
};

export default RiskGauge;