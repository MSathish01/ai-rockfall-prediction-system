import React from 'react';
import { Row, Col } from 'react-bootstrap';
import { FaBell, FaExclamationTriangle, FaCheckCircle, FaClock } from 'react-icons/fa';

const QuickStats = ({ alerts, riskAssessment }) => {
  const totalAlerts = alerts ? alerts.length : 0;
  const activeAlerts = alerts ? alerts.filter(alert => alert.status === 'ACTIVE').length : 0;
  const highRiskAlerts = alerts ? alerts.filter(alert => 
    alert.severity === 'HIGH' || alert.severity === 'CRITICAL'
  ).length : 0;

  const stats = [
    {
      icon: FaBell,
      value: totalAlerts,
      label: 'Total Alerts',
      color: 'primary'
    },
    {
      icon: FaExclamationTriangle,
      value: activeAlerts,
      label: 'Active Alerts',
      color: 'warning'
    },
    {
      icon: FaExclamationTriangle,
      value: highRiskAlerts,
      label: 'High Risk',
      color: 'danger'
    },
    {
      icon: riskAssessment?.risk_level === 'LOW' ? FaCheckCircle : FaClock,
      value: riskAssessment?.risk_level || 'N/A',
      label: 'Current Risk',
      color: riskAssessment?.risk_level === 'LOW' ? 'success' : 'warning'
    }
  ];

  return (
    <Row>
      {stats.map((stat, index) => (
        <Col xs={6} key={index} className="mb-3">
          <div className="text-center">
            <stat.icon className={`text-${stat.color} mb-2`} size={24} />
            <div className="fw-bold">{stat.value}</div>
            <small className="text-muted">{stat.label}</small>
          </div>
        </Col>
      ))}
    </Row>
  );
};

export default QuickStats;