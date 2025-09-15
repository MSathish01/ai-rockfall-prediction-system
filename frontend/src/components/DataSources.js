import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button, Modal, Form, Alert, ProgressBar, Tabs, Tab } from 'react-bootstrap';
import { FaCamera, FaUpload, FaMap, FaCloudUploadAlt, FaSatellite, FaImage, FaFileImage, FaEye, FaDownload, FaSync, FaTrash } from 'react-icons/fa';
import axios from 'axios';

const DataSources = () => {
  const [activeTab, setActiveTab] = useState('drone');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadType, setUploadType] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [dataSources, setDataSources] = useState({
    drone: [],
    dem: [],
    satellite: [],
    geological: []
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDataSources();
  }, []);

  const fetchDataSources = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/data-sources');
      setDataSources(response.data);
      setError(null);
    } catch (err) {
      // Mock data for demonstration
      setDataSources({
        drone: [
          {
            id: 1,
            filename: 'drone_survey_zone_a_20240115.jpg',
            type: 'RGB',
            timestamp: new Date().toISOString(),
            location: { lat: -23.5505, lng: -46.6333 },
            altitude: 150,
            resolution: '4K',
            size: '12.5 MB',
            status: 'processed',
            analysis: {
              cracks_detected: 3,
              vegetation_coverage: 15,
              slope_angle: 45,
              risk_indicators: ['visible_fractures', 'loose_rocks']
            }
          },
          {
            id: 2,
            filename: 'thermal_survey_zone_b_20240115.tiff',
            type: 'Thermal',
            timestamp: new Date(Date.now() - 3600000).toISOString(),
            location: { lat: -23.5515, lng: -46.6343 },
            altitude: 120,
            resolution: '1080p',
            size: '8.2 MB',
            status: 'processing',
            analysis: {
              temperature_anomalies: 2,
              moisture_areas: 5,
              thermal_gradient: 'moderate'
            }
          }
        ],
        dem: [
          {
            id: 1,
            filename: 'dem_mine_site_2024_v2.tif',
            type: 'Digital Elevation Model',
            timestamp: new Date(Date.now() - 86400000).toISOString(),
            resolution: '1m',
            coverage: '500 hectares',
            size: '245 MB',
            status: 'active',
            analysis: {
              slope_stability: 'moderate_risk',
              elevation_change: '+2.3m',
              volume_calculation: '15,000 m³'
            }
          }
        ],
        satellite: [
          {
            id: 1,
            filename: 'sentinel2_20240110.tif',
            type: 'Multispectral',
            timestamp: new Date(Date.now() - 432000000).toISOString(),
            resolution: '10m',
            bands: 13,
            size: '156 MB',
            status: 'processed',
            analysis: {
              vegetation_index: 0.65,
              moisture_content: 'low',
              land_cover_change: 'minimal'
            }
          }
        ],
        geological: [
          {
            id: 1,
            filename: 'geological_survey_2024.shp',
            type: 'Geological Map',
            timestamp: new Date(Date.now() - 2592000000).toISOString(),
            features: 156,
            rock_types: ['granite', 'schist', 'quartzite'],
            size: '5.2 MB',
            status: 'active',
            analysis: {
              fault_lines: 8,
              joint_sets: 3,
              weathering_grade: 'moderate'
            }
          }
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = (type) => {
    setUploadType(type);
    setShowUploadModal(true);
  };

  const simulateUpload = () => {
    setUploadProgress(0);
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setShowUploadModal(false);
          fetchDataSources(); // Refresh data
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const getStatusBadge = (status) => {
    const variants = {
      'processed': 'success',
      'processing': 'warning',
      'active': 'primary',
      'error': 'danger'
    };
    return <Badge bg={variants[status] || 'secondary'}>{status.toUpperCase()}</Badge>;
  };

  const getTypeIcon = (type) => {
    const icons = {
      'drone': <FaCamera />,
      'dem': <FaMap />,
      'satellite': <FaSatellite />,
      'geological': <FaImage />
    };
    return icons[type] || <FaFileImage />;
  };

  const renderDataTable = (data, type) => (
    <Table responsive striped hover>
      <thead className="table-dark">
        <tr>
          <th>File</th>
          <th>Type</th>
          <th>Timestamp</th>
          <th>Details</th>
          <th>Status</th>
          <th>Analysis</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            <td>
              <div className="d-flex align-items-center">
                {getTypeIcon(type)}
                <div className="ms-2">
                  <div className="fw-bold">{item.filename}</div>
                  <small className="text-muted">{item.size}</small>
                </div>
              </div>
            </td>
            <td>
              <Badge bg="info">{item.type}</Badge>
            </td>
            <td>
              <small>{new Date(item.timestamp).toLocaleString()}</small>
            </td>
            <td>
              {type === 'drone' && (
                <div>
                  <small>Alt: {item.altitude}m</small><br />
                  <small>Res: {item.resolution}</small>
                </div>
              )}
              {type === 'dem' && (
                <div>
                  <small>Res: {item.resolution}</small><br />
                  <small>Area: {item.coverage}</small>
                </div>
              )}
              {type === 'satellite' && (
                <div>
                  <small>Res: {item.resolution}</small><br />
                  <small>Bands: {item.bands}</small>
                </div>
              )}
              {type === 'geological' && (
                <div>
                  <small>Features: {item.features}</small><br />
                  <small>Types: {item.rock_types?.join(', ')}</small>
                </div>
              )}
            </td>
            <td>{getStatusBadge(item.status)}</td>
            <td>
              {item.analysis && (
                <div>
                  {Object.entries(item.analysis).slice(0, 2).map(([key, value]) => (
                    <div key={key}>
                      <small><strong>{key.replace('_', ' ')}:</strong> {value}</small>
                    </div>
                  ))}
                </div>
              )}
            </td>
            <td>
              <Button variant="outline-primary" size="sm" className="me-1">
                <FaEye />
              </Button>
              <Button variant="outline-success" size="sm" className="me-1">
                <FaDownload />
              </Button>
              <Button variant="outline-danger" size="sm">
                <FaTrash />
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );

  return (
    <Container fluid className="mt-4">
      <Row className="mb-4">
        <Col>
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="display-5">
                <FaCloudUploadAlt className="me-3" />
                Multi-Source Data Integration
              </h1>
              <p className="lead">Manage drone imagery, DEM data, satellite images, and geological surveys</p>
            </div>
            <div>
              <Button variant="success" onClick={fetchDataSources} className="me-2">
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
            <Alert variant="danger">{error}</Alert>
          </Col>
        </Row>
      )}

      {/* Data Source Statistics */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaCamera size={32} className="text-primary mb-2" />
              <h4>{dataSources.drone?.length || 0}</h4>
              <small>Drone Images</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaMap size={32} className="text-success mb-2" />
              <h4>{dataSources.dem?.length || 0}</h4>
              <small>DEM Files</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaSatellite size={32} className="text-info mb-2" />
              <h4>{dataSources.satellite?.length || 0}</h4>
              <small>Satellite Images</small>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="text-center">
            <Card.Body>
              <FaImage size={32} className="text-warning mb-2" />
              <h4>{dataSources.geological?.length || 0}</h4>
              <small>Geological Data</small>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Data Sources Tabs */}
      <Row>
        <Col>
          <Card>
            <Card.Header>
              <Tabs activeKey={activeTab} onSelect={setActiveTab} className="card-header-tabs">
                <Tab eventKey="drone" title={
                  <span><FaCamera className="me-2" />Drone Imagery</span>
                }>
                </Tab>
                <Tab eventKey="dem" title={
                  <span><FaMap className="me-2" />DEM Data</span>
                }>
                </Tab>
                <Tab eventKey="satellite" title={
                  <span><FaSatellite className="me-2" />Satellite</span>
                }>
                </Tab>
                <Tab eventKey="geological" title={
                  <span><FaImage className="me-2" />Geological</span>
                }>
                </Tab>
              </Tabs>
            </Card.Header>
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h5 className="mb-0">
                  {activeTab === 'drone' && 'Drone Imagery & Aerial Surveys'}
                  {activeTab === 'dem' && 'Digital Elevation Models'}
                  {activeTab === 'satellite' && 'Satellite Imagery'}
                  {activeTab === 'geological' && 'Geological Survey Data'}
                </h5>
                <Button 
                  variant="primary" 
                  onClick={() => handleUpload(activeTab)}
                >
                  <FaUpload className="me-1" />
                  Upload {activeTab === 'drone' ? 'Images' : activeTab === 'dem' ? 'DEM' : activeTab === 'satellite' ? 'Satellite Data' : 'Geological Data'}
                </Button>
              </div>

              {loading ? (
                <div className="text-center py-4">
                  <div className="spinner-border" role="status">
                    <span className="visually-hidden">Loading...</span>
                  </div>
                </div>
              ) : (
                <>
                  {activeTab === 'drone' && renderDataTable(dataSources.drone || [], 'drone')}
                  {activeTab === 'dem' && renderDataTable(dataSources.dem || [], 'dem')}
                  {activeTab === 'satellite' && renderDataTable(dataSources.satellite || [], 'satellite')}
                  {activeTab === 'geological' && renderDataTable(dataSources.geological || [], 'geological')}
                </>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Upload Modal */}
      <Modal show={showUploadModal} onHide={() => setShowUploadModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            <FaUpload className="me-2" />
            Upload {uploadType.charAt(0).toUpperCase() + uploadType.slice(1)} Data
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Select Files</Form.Label>
              <Form.Control type="file" multiple accept={
                uploadType === 'drone' ? 'image/*,.tiff,.tif' :
                uploadType === 'dem' ? '.tif,.tiff,.asc,.xyz' :
                uploadType === 'satellite' ? '.tif,.tiff,.jp2' :
                '.shp,.kml,.gpx,.geojson'
              } />
              <Form.Text className="text-muted">
                {uploadType === 'drone' && 'Supported: JPG, PNG, TIFF, GeoTIFF'}
                {uploadType === 'dem' && 'Supported: GeoTIFF, ASCII Grid, XYZ'}
                {uploadType === 'satellite' && 'Supported: GeoTIFF, JPEG2000'}
                {uploadType === 'geological' && 'Supported: Shapefile, KML, GPX, GeoJSON'}
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Location</Form.Label>
              <Row>
                <Col>
                  <Form.Control type="number" placeholder="Latitude" step="0.000001" />
                </Col>
                <Col>
                  <Form.Control type="number" placeholder="Longitude" step="0.000001" />
                </Col>
              </Row>
            </Form.Group>

            {uploadType === 'drone' && (
              <>
                <Form.Group className="mb-3">
                  <Form.Label>Flight Details</Form.Label>
                  <Row>
                    <Col>
                      <Form.Control type="number" placeholder="Altitude (m)" />
                    </Col>
                    <Col>
                      <Form.Select>
                        <option>Camera Type</option>
                        <option>RGB</option>
                        <option>Thermal</option>
                        <option>Multispectral</option>
                        <option>LiDAR</option>
                      </Form.Select>
                    </Col>
                  </Row>
                </Form.Group>
              </>
            )}

            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control as="textarea" rows={3} placeholder="Add description or notes..." />
            </Form.Group>

            {uploadProgress > 0 && (
              <div className="mb-3">
                <div className="d-flex justify-content-between mb-1">
                  <small>Upload Progress</small>
                  <small>{uploadProgress}%</small>
                </div>
                <ProgressBar now={uploadProgress} />
              </div>
            )}
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowUploadModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={simulateUpload}>
            <FaUpload className="me-1" />
            Start Upload
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
};

export default DataSources;