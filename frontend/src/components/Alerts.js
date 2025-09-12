import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button, Alert as BootstrapAlert } from 'react-bootstrap';
import { FaBell, FaSync, FaFilter } from 'react-icons/fa';
import axios from 'axios';
import moment from 'moment';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('ALL');

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await axios.get('/api/alerts');
      setAlerts(response.data.alerts);
      setError(null);
    } catch (err) {
      setError('Failed to fetch alerts');
      console.error('Alerts error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityVariant = (severity) => {
    switch (severity) {
      case 'LOW': return 'success';
      case 'MEDIUM': return 'warning';
      case 'HIGH': return 'danger';
      case 'CRITICAL': return 'dark';
      default: return 'secondary';
    }
  };

  const getStatusVariant = (status) => {
    switch (status) {
      case 'ACTIVE': return 'danger';
      case 'ACKNOWLEDGED': return 'warning';
      case 'RESOLVED': return 'success';
      default: return 'secondary';
    }
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filter === 'ALL') return true;
    if (filter === 'ACTIVE') return alert.status === 'ACTIVE';
    if (filter === 'HIGH_RISK') return alert.severity === 'HIGH' || alert.severity === 'CRITICAL';
    return true;
  });

  if (loading) {
    return (
      <Container className="mt-4">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </Container>
    );
  }

  return (
    <Container fluid className="mt-4">
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="display-5">
                <FaBell className="me-3" />
                Alert Management
              </h1>
              <p className="lead">Monitor and manage system alerts</p>
            </div>
            <div>
              <Button variant="outline-primary" onClick={() => setFilter('ALL')} className={filter === 'ALL' ? 'active' : ''}>
                All
              </Button>
              <Button variant="outline-warning" onClick={() => setFilter('ACTIVE')} className={`ms-2 ${filter === 'ACTIVE' ? 'active' : ''}`}>
                Active
              </Button>
              <Button variant="outline-danger" onClick={() => setFilter('HIGH_RISK')} className={`ms-2 ${filter === 'HIGH_RISK' ? 'active' : ''}`}>
                High Risk
              </Button>
              <Button variant="success" onClick={fetchAlerts} className="ms-3">
                <FaSync className="me-1" />
                Refresh
              </Button>
            </div>
          </div>
        </Col>
      </Row>

      {error && (
        <Row className="mb-4">
          <Col>
            <BootstrapAlert variant="danger">{error}</BootstrapAlert>
          </Col>
        </Row>
      )}

      <Row className="mb-4">
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-primary">{alerts.length}</h4>
              <small>Total Alerts</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-danger">{alerts.filter(a => a.status === 'ACTIVE').length}</h4>
              <small>Active Alerts</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-warning">{alerts.filter(a => a.severity === 'HIGH' || a.severity === 'CRITICAL').length}</h4>
              <small>High Risk</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-success">{alerts.filter(a => a.status === 'RESOLVED').length}</h4>
              <small>Resolved</small>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card>
            <Card.Header>
              <h5 className="mb-0">
                <FaFilter className="me-2" />
                Alerts ({filteredAlerts.length})
              </h5>
            </Card.Header>
            <Card.Body className="p-0">
              {filteredAlerts.length > 0 ? (
                <Table responsive striped hover className="mb-0">
                  <thead className="table-dark">
                    <tr>
                      <th>Timestamp</th>
                      <th>Type</th>
                      <th>Severity</th>
                      <th>Status</th>
                      <th>Message</th>
                      <th>Location</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredAlerts.map((alert) => (
                      <tr key={alert.id}>
                        <td>
                          <small>{moment(alert.timestamp).format('YYYY-MM-DD HH:mm:ss')}</small>
                          <br />
                          <small className="text-muted">{moment(alert.timestamp).fromNow()}</small>
                        </td>
                        <td>
                          <Badge bg="info">{alert.alert_type}</Badge>
                        </td>
                        <td>
                          <Badge bg={getSeverityVariant(alert.severity)}>
                            {alert.severity}
                          </Badge>
                        </td>
                        <td>
                          <Badge bg={getStatusVariant(alert.status)}>
                            {alert.status}
                          </Badge>
                        </td>
                        <td>{alert.message}</td>
                        <td>
                          {alert.location ? (
                            <small className="text-muted">
                              Coordinates available
                            </small>
                          ) : (
                            <small className="text-muted">N/A</small>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              ) : (
                <div className="text-center p-4">
                  <FaBell size={48} className="text-muted mb-3" />
                  <p className="text-muted">No alerts match the current filter</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Alerts;