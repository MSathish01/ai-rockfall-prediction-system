import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Alert, Button, ButtonGroup } from 'react-bootstrap';
import { MapContainer, TileLayer, Circle, Popup, Marker } from 'react-leaflet';
import { FaMap, FaSync, FaDownload } from 'react-icons/fa';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const RiskMap = () => {
  const [riskZones, setRiskZones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [mapView, setMapView] = useState('risk'); // 'risk', 'sensors', 'alerts'
  const [lastUpdate, setLastUpdate] = useState(null);

  // Default center coordinates (can be configured for specific mine location)
  const defaultCenter = [-23.5505, -46.6333];
  const defaultZoom = 15;

  useEffect(() => {
    fetchRiskMapData();
    const interval = setInterval(fetchRiskMapData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  const fetchRiskMapData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/risk-map');
      setRiskZones(response.data.risk_zones);
      setLastUpdate(new Date(response.data.timestamp));
      setError(null);
    } catch (err) {
      setError('Failed to fetch risk map data');
      console.error('Risk map error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'LOW': return '#28a745';
      case 'MEDIUM': return '#ffc107';
      case 'HIGH': return '#fd7e14';
      case 'CRITICAL': return '#dc3545';
      default: return '#6c757d';
    }
  };

  const getRiskRadius = (riskValue) => {
    return Math.max(20, riskValue * 100); // Minimum 20m, max 100m radius
  };

  const exportMapData = () => {
    const dataStr = JSON.stringify(riskZones, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `risk_map_${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <Container fluid className="mt-4">
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="display-5">
                <FaMap className="me-3" />
                Risk Map
              </h1>
              <p className="lead">Real-time visualization of rockfall risk zones</p>
            </div>
            <div>
              <ButtonGroup className="me-2">
                <Button 
                  variant={mapView === 'risk' ? 'primary' : 'outline-primary'}
                  onClick={() => setMapView('risk')}
                >
                  Risk Zones
                </Button>
                <Button 
                  variant={mapView === 'sensors' ? 'primary' : 'outline-primary'}
                  onClick={() => setMapView('sensors')}
                >
                  Sensors
                </Button>
              </ButtonGroup>
              <Button variant="success" onClick={fetchRiskMapData} className="me-2">
                <FaSync className="me-1" />
                Refresh
              </Button>
              <Button variant="info" onClick={exportMapData}>
                <FaDownload className="me-1" />
                Export
              </Button>
            </div>
          </div>
        </Col>
      </Row>

      {error && (
        <Row className="mb-4">
          <Col>
            <Alert variant="danger">{error}</Alert>
          </Col>
        </Row>
      )}

      <Row>
        <Col lg={9}>
          <Card>
            <Card.Header>
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="mb-0">Interactive Risk Map</h5>
                {lastUpdate && (
                  <small className="text-muted">
                    Last updated: {lastUpdate.toLocaleString()}
                  </small>
                )}
              </div>
            </Card.Header>
            <Card.Body style={{ height: '600px', padding: 0 }}>
              {loading ? (
                <div className="d-flex justify-content-center align-items-center h-100">
                  <div className="spinner-border" role="status">
                    <span className="visually-hidden">Loading map...</span>
                  </div>
                </div>
              ) : (
                <MapContainer
                  center={defaultCenter}
                  zoom={defaultZoom}
                  style={{ height: '100%', width: '100%' }}
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  />
                  
                  {riskZones.map((zone, index) => (
                    <Circle
                      key={index}
                      center={[zone.lat, zone.lng]}
                      radius={getRiskRadius(zone.risk_value)}
                      pathOptions={{
                        color: getRiskColor(zone.risk_level),
                        fillColor: getRiskColor(zone.risk_level),
                        fillOpacity: 0.4,
                        weight: 2
                      }}
                    >
                      <Popup>
                        <div>
                          <h6>Risk Zone {index + 1}</h6>
                          <p><strong>Risk Level:</strong> {zone.risk_level}</p>
                          <p><strong>Risk Value:</strong> {(zone.risk_value * 100).toFixed(1)}%</p>
                          <p><strong>Coordinates:</strong> {zone.lat.toFixed(4)}, {zone.lng.toFixed(4)}</p>
                        </div>
                      </Popup>
                    </Circle>
                  ))}
                  
                  {/* Add sensor markers if in sensor view */}
                  {mapView === 'sensors' && (
                    <>
                      <Marker position={[-23.5505, -46.6333]}>
                        <Popup>
                          <div>
                            <h6>Displacement Sensor DS-001</h6>
                            <p>Status: Active</p>
                            <p>Last Reading: 0.8mm</p>
                          </div>
                        </Popup>
                      </Marker>
                      <Marker position={[-23.5515, -46.6343]}>
                        <Popup>
                          <div>
                            <h6>Strain Gauge SG-002</h6>
                            <p>Status: Active</p>
                            <p>Last Reading: 120 μstrain</p>
                          </div>
                        </Popup>
                      </Marker>
                    </>
                  )}
                </MapContainer>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col lg={3}>
          <Card className="mb-3">
            <Card.Header>
              <h6 className="mb-0">Risk Legend</h6>
            </Card.Header>
            <Card.Body>
              <div className="d-flex align-items-center mb-2">
                <div 
                  style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#28a745', 
                    marginRight: '10px',
                    borderRadius: '50%'
                  }}
                ></div>
                <span>Low Risk (0-25%)</span>
              </div>
              <div className="d-flex align-items-center mb-2">
                <div 
                  style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#ffc107', 
                    marginRight: '10px',
                    borderRadius: '50%'
                  }}
                ></div>
                <span>Medium Risk (25-50%)</span>
              </div>
              <div className="d-flex align-items-center mb-2">
                <div 
                  style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#fd7e14', 
                    marginRight: '10px',
                    borderRadius: '50%'
                  }}
                ></div>
                <span>High Risk (50-75%)</span>
              </div>
              <div className="d-flex align-items-center">
                <div 
                  style={{ 
                    width: '20px', 
                    height: '20px', 
                    backgroundColor: '#dc3545', 
                    marginRight: '10px',
                    borderRadius: '50%'
                  }}
                ></div>
                <span>Critical Risk (75-100%)</span>
              </div>
            </Card.Body>
          </Card>

          <Card>
            <Card.Header>
              <h6 className="mb-0">Zone Statistics</h6>
            </Card.Header>
            <Card.Body>
              {riskZones.length > 0 ? (
                <>
                  <p><strong>Total Zones:</strong> {riskZones.length}</p>
                  <p><strong>High Risk Zones:</strong> {riskZones.filter(z => z.risk_level === 'HIGH' || z.risk_level === 'CRITICAL').length}</p>
                  <p><strong>Average Risk:</strong> {(riskZones.reduce((sum, z) => sum + z.risk_value, 0) / riskZones.length * 100).toFixed(1)}%</p>
                  <p><strong>Max Risk:</strong> {(Math.max(...riskZones.map(z => z.risk_value)) * 100).toFixed(1)}%</p>
                </>
              ) : (
                <p>No zone data available</p>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default RiskMap;