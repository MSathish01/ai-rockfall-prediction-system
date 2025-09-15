import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Badge, ProgressBar, Alert } from 'react-bootstrap';
import { FaDatabase, FaSync, FaCheckCircle, FaExclamationTriangle, FaClock } from 'react-icons/fa';

const DataIntegration = () => {
  const [integrationStatus, setIntegrationStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntegrationStatus();
    const interval = setInterval(fetchIntegrationStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchIntegrationStatus = async () => {
    try {
      // Mock integration status
      setIntegrationStatus({
        overall_health: 'good',
        data_sources: {
          sensors: { status: 'active', last_update: '2 minutes ago', count: 12 },
          drone: { status: 'active', last_update: '15 minutes ago', count: 8 },
          dem: { status: 'active', last_update: '1 hour ago', count: 3 },
          satellite: { status: 'processing', last_update: '3 hours ago', count: 5 },
          geological: { status: 'active', last_update: '1 day ago', count: 2 }
        },
        integration_metrics: {
          data_fusion_accuracy: 94.2,
          processing_speed: 87.5,
          storage_efficiency: 91.8,
          prediction_confidence: 89.3
        }
      });
    } catch (error) {
      console.error('Failed to fetch integration status:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active': return <FaCheckCircle className="text-success" />;
      case 'processing': return <FaSync className="text-warning" />;
      case 'error': return <FaExclamationTriangle className="text-danger" />;
      default: return <FaClock className="text-secondary" />;
    }
  };

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
          <h2>
            <FaDatabase className="me-2" />
            Multi-Source Data Integration Status
          </h2>
        </Col>
      </Row>

      {integrationStatus && (
        <>
          <Row className="mb-4">
            <Col>
              <Alert variant={integrationStatus.overall_health === 'good' ? 'success' : 'warning'}>
                <strong>System Health: </strong>
                {integrationStatus.overall_health === 'good' ? 'All systems operational' : 'Some issues detected'}
              </Alert>
            </Col>
          </Row>

          <Row className="mb-4">
            {Object.entries(integrationStatus.data_sources).map(([source, data]) => (
              <Col md={6} lg={4} key={source} className="mb-3">
                <Card>
                  <Card.Body>
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <h6 className="mb-0">{source.toUpperCase()}</h6>
                      {getStatusIcon(data.status)}
                    </div>
                    <p className="mb-1">
                      <strong>Count:</strong> {data.count} sources
                    </p>
                    <p className="mb-0 text-muted">
                      <small>Last update: {data.last_update}</small>
                    </p>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>

          <Row>
            <Col>
              <Card>
                <Card.Header>
                  <h5 className="mb-0">Integration Performance Metrics</h5>
                </Card.Header>
                <Card.Body>
                  {Object.entries(integrationStatus.integration_metrics).map(([metric, value]) => (
                    <div key={metric} className="mb-3">
                      <div className="d-flex justify-content-between mb-1">
                        <span>{metric.replace('_', ' ').toUpperCase()}</span>
                        <span>{value}%</span>
                      </div>
                      <ProgressBar 
                        now={value} 
                        variant={value > 90 ? 'success' : value > 70 ? 'warning' : 'danger'}
                      />
                    </div>
                  ))}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
};

export default DataIntegration;