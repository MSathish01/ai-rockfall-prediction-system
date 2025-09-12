import React from 'react';
import { ListGroup, Badge } from 'react-bootstrap';
import { FaExclamationTriangle, FaClock } from 'react-icons/fa';
import moment from 'moment';

const RecentAlerts = ({ alerts }) => {
  const getSeverityVariant = (severity) => {
    switch (severity) {
      case 'LOW': return 'success';
      case 'MEDIUM': return 'warning';
      case 'HIGH': return 'danger';
      case 'CRITICAL': return 'dark';
      default: return 'secondary';
    }
  };

  if (!alerts || alerts.length === 0) {
    return (
      <div className="text-center text-muted">
        <FaExclamationTriangle className="mb-2" size={24} />
        <p>No recent alerts</p>
      </div>
    );
  }

  return (
    <ListGroup variant="flush">
      {alerts.map((alert) => (
        <ListGroup.Item key={alert.id} className="px-0">
          <div className="d-flex justify-content-between align-items-start">
            <div className="flex-grow-1">
              <div className="d-flex align-items-center mb-1">
                <Badge bg={getSeverityVariant(alert.severity)} className="me-2">
                  {alert.severity}
                </Badge>
                <small className="text-muted">
                  <FaClock className="me-1" />
                  {moment(alert.timestamp).fromNow()}
                </small>
              </div>
              <p className="mb-0 small">{alert.message}</p>
            </div>
          </div>
        </ListGroup.Item>
      ))}
    </ListGroup>
  );
};

export default RecentAlerts;