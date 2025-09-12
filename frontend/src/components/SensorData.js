import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button } from 'react-bootstrap';
import { FaCog, FaSync, FaPlay, FaStop } from 'react-icons/fa';

const SensorData = () => {
  const [sensors, setSensors] = useState([]);
  const [simulatorStatus, setSimulatorStatus] = useState('stopped');

  useEffect(() => {
    // Initialize mock sensor data
    const mockSensors = [
      {
        id: 'DS-001',
        name: 'Displacement Sensor 1',
        type: 'displacement',
        location: 'Zone A - North Wall',
        status: 'active',
        lastReading: '0.8 mm',
        lastUpdate: new Date().toISOString(),
        batteryLevel: 85,
        coordinates: { lat: -23.5505, lng: -46.6333 }
      },
      {
        id: 'SG-002',
        name: 'Strain Gauge 2',
        type: 'strain',
        location: 'Zone B - East Wall',
        status: 'active',
        lastReading: '120 μstrain',
        lastUpdate: new Date().toISOString(),
        batteryLevel: 92,
        coordinates: { lat: -23.5515, lng: -46.6343 }
      },
      {
        id: 'PP-003',
        name: 'Pore Pressure Monitor 3',
        type: 'pore_pressure',
        location: 'Zone C - South Wall',
        status: 'active',
        lastReading: '60 kPa',
        lastUpdate: new Date().toISOString(),
        batteryLevel: 78,
        coordinates: { lat: -23.5525, lng: -46.6353 }
      },
      {
        id: 'TM-004',
        name: 'Temperature Monitor 4',
        type: 'temperature',
        location: 'Weather Station',
        status: 'active',
        lastReading: '18°C',
        lastUpdate: new Date().toISOString(),
        batteryLevel: 95,
        coordinates: { lat: -23.5535, lng: -46.6363 }
      },
      {
        id: 'RG-005',
        name: 'Rain Gauge 5',
        type: 'rainfall',
        location: 'Weather Station',
        status: 'active',
        lastReading: '2.5 mm/h',
        lastUpdate: new Date().toISOString(),
        batteryLevel: 88,
        coordinates: { lat: -23.5545, lng: -46.6373 }
      },
      {
        id: 'VM-006',
        name: 'Vibration Monitor 6',
        type: 'vibration',
        location: 'Zone D - West Wall',
        status: 'maintenance',
        lastReading: '0.05 m/s²',
        lastUpdate: new Date(Date.now() - 3600000).toISOString(),
        batteryLevel: 45,
        coordinates: { lat: -23.5555, lng: -46.6383 }
      }
    ];
    
    setSensors(mockSensors);
  }, []);

  const getStatusVariant = (status) => {
    switch (status) {
      case 'active': return 'success';
      case 'warning': return 'warning';
      case 'maintenance': return 'danger';
      case 'offline': return 'secondary';
      default: return 'secondary';
    }
  };

  const getBatteryColor = (level) => {
    if (level > 70) return 'success';
    if (level > 30) return 'warning';
    return 'danger';
  };

  const getSensorTypeIcon = (type) => {
    switch (type) {
      case 'displacement': return '📏';
      case 'strain': return '🔧';
      case 'pore_pressure': return '💧';
      case 'temperature': return '🌡️';
      case 'rainfall': return '🌧️';
      case 'vibration': return '📳';
      default: return '📊';
    }
  };

  const startSimulator = () => {
    setSimulatorStatus('running');
    // In a real implementation, this would start the sensor simulator
    console.log('Starting sensor simulator...');
  };

  const stopSimulator = () => {
    setSimulatorStatus('stopped');
    // In a real implementation, this would stop the sensor simulator
    console.log('Stopping sensor simulator...');
  };

  const refreshSensors = () => {
    // Simulate data refresh
    setSensors(prevSensors => 
      prevSensors.map(sensor => ({
        ...sensor,
        lastUpdate: new Date().toISOString(),
        batteryLevel: Math.max(20, sensor.batteryLevel - Math.random() * 2)
      }))
    );
  };

  return (
    <Container fluid className="mt-4">
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="display-5">
                <FaCog className="me-3" />
                Sensor Management
              </h1>
              <p className="lead">Monitor and manage sensor network</p>
            </div>
            <div>
              {simulatorStatus === 'stopped' ? (
                <Button variant="success" onClick={startSimulator} className="me-2">
                  <FaPlay className="me-1" />
                  Start Simulator
                </Button>
              ) : (
                <Button variant="danger" onClick={stopSimulator} className="me-2">
                  <FaStop className="me-1" />
                  Stop Simulator
                </Button>
              )}
              <Button variant="primary" onClick={refreshSensors}>
                <FaSync className="me-1" />
                Refresh
              </Button>
            </div>
          </div>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-primary">{sensors.length}</h4>
              <small>Total Sensors</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-success">{sensors.filter(s => s.status === 'active').length}</h4>
              <small>Active Sensors</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-warning">{sensors.filter(s => s.batteryLevel < 50).length}</h4>
              <small>Low Battery</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card>
            <Card.Body className="text-center">
              <h4 className="text-danger">{sensors.filter(s => s.status === 'maintenance').length}</h4>
              <small>Maintenance Required</small>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <Card>
            <Card.Header className="d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Sensor Status</h5>
              <Badge bg={simulatorStatus === 'running' ? 'success' : 'secondary'}>
                Simulator: {simulatorStatus}
              </Badge>
            </Card.Header>
            <Card.Body className="p-0">
              <Table responsive striped hover className="mb-0">
                <thead className="table-dark">
                  <tr>
                    <th>Sensor</th>
                    <th>Type</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Last Reading</th>
                    <th>Battery</th>
                    <th>Last Update</th>
                  </tr>
                </thead>
                <tbody>
                  {sensors.map((sensor) => (
                    <tr key={sensor.id}>
                      <td>
                        <div className="d-flex align-items-center">
                          <span className="me-2">{getSensorTypeIcon(sensor.type)}</span>
                          <div>
                            <div className="fw-bold">{sensor.id}</div>
                            <small className="text-muted">{sensor.name}</small>
                          </div>
                        </div>
                      </td>
                      <td>
                        <Badge bg="info">{sensor.type}</Badge>
                      </td>
                      <td>{sensor.location}</td>
                      <td>
                        <Badge bg={getStatusVariant(sensor.status)}>
                          {sensor.status.toUpperCase()}
                        </Badge>
                      </td>
                      <td className="fw-bold">{sensor.lastReading}</td>
                      <td>
                        <div className="d-flex align-items-center">
                          <div 
                            className={`badge bg-${getBatteryColor(sensor.batteryLevel)} me-2`}
                            style={{ minWidth: '45px' }}
                          >
                            {sensor.batteryLevel}%
                          </div>
                          <div 
                            className="progress" 
                            style={{ width: '60px', height: '8px' }}
                          >
                            <div 
                              className={`progress-bar bg-${getBatteryColor(sensor.batteryLevel)}`}
                              style={{ width: `${sensor.batteryLevel}%` }}
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td>
                        <small>
                          {new Date(sensor.lastUpdate).toLocaleString()}
                        </small>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md={6}>
          <Card>
            <Card.Header>
              <h6 className="mb-0">Sensor Network Map</h6>
            </Card.Header>
            <Card.Body>
              <div className="text-center text-muted">
                <FaCog size={48} className="mb-3" />
                <p>Interactive sensor map would be displayed here</p>
                <small>Shows real-time sensor locations and status</small>
              </div>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card>
            <Card.Header>
              <h6 className="mb-0">Maintenance Schedule</h6>
            </Card.Header>
            <Card.Body>
              <Table size="sm">
                <thead>
                  <tr>
                    <th>Sensor</th>
                    <th>Next Maintenance</th>
                    <th>Priority</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>VM-006</td>
                    <td>Overdue</td>
                    <td><Badge bg="danger">High</Badge></td>
                  </tr>
                  <tr>
                    <td>PP-003</td>
                    <td>2 days</td>
                    <td><Badge bg="warning">Medium</Badge></td>
                  </tr>
                  <tr>
                    <td>DS-001</td>
                    <td>1 week</td>
                    <td><Badge bg="success">Low</Badge></td>
                  </tr>
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default SensorData;