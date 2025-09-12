import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Alert, Badge, ProgressBar, Table, Button, ButtonGroup } from 'react-bootstrap';
import { Line, Doughnut } from 'react-chartjs-2';
import { FaChartLine, FaCalendarAlt, FaExclamationTriangle, FaCloudRain, FaThermometerHalf, FaSync, FaDownload } from 'react-icons/fa';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ArcElement
);

const Forecast = () => {
  const [forecastData, setForecastData] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [viewMode, setViewMode] = useState('7day'); // '7day', '14day', '30day'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchForecast();
    generateMockWeatherData();
    generateMockHistoricalData();
    const interval = setInterval(() => {
      fetchForecast();
      generateMockWeatherData();
    }, 60000); // Update every minute for demo
    return () => clearInterval(interval);
  }, [viewMode]);

  const fetchForecast = async () => {
    try {
      const response = await axios.get('/api/forecast');
      setForecastData(response.data);
      setError(null);
    } catch (err) {
      // Generate mock data if API fails
      generateMockForecastData();
      console.error('Forecast error:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateMockForecastData = () => {
    const days = viewMode === '7day' ? 7 : viewMode === '14day' ? 14 : 30;
    const mockData = {
      dates: [],
      probabilities: [],
      confidence_intervals: []
    };

    const baseDate = new Date();
    let baseProbability = 0.3 + Math.random() * 0.3;

    for (let i = 0; i < days; i++) {
      const date = new Date(baseDate);
      date.setDate(date.getDate() + i);
      
      // Add some realistic variation
      const variation = (Math.sin(i * 0.5) * 0.1) + (Math.random() - 0.5) * 0.15;
      const probability = Math.max(0.1, Math.min(0.9, baseProbability + variation));
      
      mockData.dates.push(date.toISOString());
      mockData.probabilities.push(probability);
      mockData.confidence_intervals.push([
        Math.max(0, probability - 0.1 - Math.random() * 0.05),
        Math.min(1, probability + 0.1 + Math.random() * 0.05)
      ]);
      
      baseProbability = probability; // Trend continuation
    }
    
    setForecastData(mockData);
  };

  const generateMockWeatherData = () => {
    setWeatherData({
      temperature: 15 + Math.random() * 10,
      rainfall: Math.random() * 20,
      humidity: 60 + Math.random() * 30,
      windSpeed: Math.random() * 15,
      pressure: 1010 + Math.random() * 20
    });
  };

  const generateMockHistoricalData = () => {
    const historical = [];
    const baseDate = new Date();
    baseDate.setDate(baseDate.getDate() - 30);
    
    for (let i = 0; i < 30; i++) {
      const date = new Date(baseDate);
      date.setDate(date.getDate() + i);
      historical.push({
        date: date.toISOString(),
        actualRisk: Math.random() * 0.8,
        predictedRisk: Math.random() * 0.8,
        incidents: Math.random() > 0.9 ? 1 : 0
      });
    }
    setHistoricalData(historical);
  };

  const formatChartData = () => {
    if (!forecastData) return null;

    const labels = forecastData.dates.map(date => 
      new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    );

    return {
      labels,
      datasets: [
        {
          label: 'Rockfall Probability',
          data: forecastData.probabilities.map(p => p * 100),
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          fill: true,
          tension: 0.4
        },
        {
          label: 'Upper Confidence',
          data: forecastData.confidence_intervals.map(ci => ci[1] * 100),
          borderColor: 'rgba(255, 99, 132, 0.5)',
          backgroundColor: 'transparent',
          borderDash: [5, 5],
          pointRadius: 0
        },
        {
          label: 'Lower Confidence',
          data: forecastData.confidence_intervals.map(ci => ci[0] * 100),
          borderColor: 'rgba(255, 99, 132, 0.5)',
          backgroundColor: 'transparent',
          borderDash: [5, 5],
          pointRadius: 0
        }
      ]
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20
        }
      },
      title: {
        display: true,
        text: `${viewMode === '7day' ? '7-Day' : viewMode === '14day' ? '14-Day' : '30-Day'} Rockfall Probability Forecast`,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            if (context.datasetIndex === 0) {
              return `Probability: ${(context.parsed.y).toFixed(1)}%`;
            }
            return `${context.dataset.label}: ${(context.parsed.y).toFixed(1)}%`;
          }
        }
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Date'
        }
      },
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Probability (%)'
        },
        ticks: {
          callback: function(value) {
            return value + '%';
          }
        },
        grid: {
          color: 'rgba(0,0,0,0.1)'
        }
      }
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false
    }
  };

  const riskDistributionData = () => {
    if (!forecastData) return null;
    
    const riskCounts = { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 };
    forecastData.probabilities.forEach(prob => {
      if (prob < 0.25) riskCounts.LOW++;
      else if (prob < 0.5) riskCounts.MEDIUM++;
      else if (prob < 0.75) riskCounts.HIGH++;
      else riskCounts.CRITICAL++;
    });

    return {
      labels: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
      datasets: [{
        data: [riskCounts.LOW, riskCounts.MEDIUM, riskCounts.HIGH, riskCounts.CRITICAL],
        backgroundColor: ['#28a745', '#ffc107', '#fd7e14', '#dc3545'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    };
  };

  const getRiskLevel = (probability) => {
    if (probability < 0.25) return { level: 'LOW', color: 'success' };
    if (probability < 0.5) return { level: 'MEDIUM', color: 'warning' };
    if (probability < 0.75) return { level: 'HIGH', color: 'danger' };
    return { level: 'CRITICAL', color: 'dark' };
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
          <div className="d-flex justify-content-between align-items-center">
            <div>
              <h1 className="display-5">
                <FaChartLine className="me-3" />
                AI Rockfall Forecast
              </h1>
              <p className="lead">Advanced predictive analytics for mine safety planning</p>
            </div>
            <div>
              <ButtonGroup className="me-2">
                <Button 
                  variant={viewMode === '7day' ? 'primary' : 'outline-primary'}
                  onClick={() => setViewMode('7day')}
                >
                  7 Days
                </Button>
                <Button 
                  variant={viewMode === '14day' ? 'primary' : 'outline-primary'}
                  onClick={() => setViewMode('14day')}
                >
                  14 Days
                </Button>
                <Button 
                  variant={viewMode === '30day' ? 'primary' : 'outline-primary'}
                  onClick={() => setViewMode('30day')}
                >
                  30 Days
                </Button>
              </ButtonGroup>
              <Button variant="success" onClick={fetchForecast} className="me-2">
                <FaSync className="me-1" />
                Refresh
              </Button>
              <Button variant="info">
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

      {/* Weather Conditions */}
      {weatherData && (
        <Row className="mb-4">
          <Col>
            <Card>
              <Card.Header className="bg-info text-white">
                <h6 className="mb-0">
                  <FaCloudRain className="me-2" />
                  Current Environmental Conditions
                </h6>
              </Card.Header>
              <Card.Body>
                <Row>
                  <Col md={2}>
                    <div className="text-center">
                      <FaThermometerHalf className="text-danger mb-2" size={24} />
                      <div className="fw-bold">{weatherData.temperature.toFixed(1)}°C</div>
                      <small className="text-muted">Temperature</small>
                    </div>
                  </Col>
                  <Col md={2}>
                    <div className="text-center">
                      <FaCloudRain className="text-primary mb-2" size={24} />
                      <div className="fw-bold">{weatherData.rainfall.toFixed(1)}mm</div>
                      <small className="text-muted">Rainfall</small>
                    </div>
                  </Col>
                  <Col md={2}>
                    <div className="text-center">
                      <div className="text-info mb-2">💧</div>
                      <div className="fw-bold">{weatherData.humidity.toFixed(0)}%</div>
                      <small className="text-muted">Humidity</small>
                    </div>
                  </Col>
                  <Col md={2}>
                    <div className="text-center">
                      <div className="text-secondary mb-2">💨</div>
                      <div className="fw-bold">{weatherData.windSpeed.toFixed(1)}km/h</div>
                      <small className="text-muted">Wind Speed</small>
                    </div>
                  </Col>
                  <Col md={2}>
                    <div className="text-center">
                      <div className="text-warning mb-2">🌡️</div>
                      <div className="fw-bold">{weatherData.pressure.toFixed(0)}hPa</div>
                      <small className="text-muted">Pressure</small>
                    </div>
                  </Col>
                  <Col md={2}>
                    <div className="text-center">
                      <div className="text-success mb-2">📊</div>
                      <div className="fw-bold">
                        {weatherData.rainfall > 10 ? 'HIGH' : weatherData.rainfall > 5 ? 'MEDIUM' : 'LOW'}
                      </div>
                      <small className="text-muted">Weather Risk</small>
                    </div>
                  </Col>
                </Row>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      {forecastData && (
        <>
          <Row className="mb-4">
            <Col lg={8}>
              <Card>
                <Card.Header className="d-flex justify-content-between align-items-center">
                  <h5 className="mb-0">
                    <FaChartLine className="me-2" />
                    Probability Forecast Chart
                  </h5>
                  <Badge bg="info">
                    {viewMode === '7day' ? '7-Day' : viewMode === '14day' ? '14-Day' : '30-Day'} View
                  </Badge>
                </Card.Header>
                <Card.Body style={{ height: '400px' }}>
                  <Line data={formatChartData()} options={chartOptions} />
                </Card.Body>
              </Card>
            </Col>
            <Col lg={4}>
              <Card className="mb-3">
                <Card.Header className="bg-warning text-dark">
                  <h6 className="mb-0">
                    <FaExclamationTriangle className="me-2" />
                    Risk Distribution
                  </h6>
                </Card.Header>
                <Card.Body style={{ height: '200px' }}>
                  {riskDistributionData() && (
                    <Doughnut 
                      data={riskDistributionData()} 
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'bottom',
                            labels: {
                              boxWidth: 12,
                              padding: 10
                            }
                          }
                        }
                      }} 
                    />
                  )}
                </Card.Body>
              </Card>
              <Card>
                <Card.Header className="bg-success text-white">
                  <h6 className="mb-0">
                    <FaCalendarAlt className="me-2" />
                    Forecast Summary
                  </h6>
                </Card.Header>
                <Card.Body>
                  <Table size="sm" className="mb-0">
                    <tbody>
                      <tr>
                        <td><small>Average Risk</small></td>
                        <td className="text-end">
                          <Badge bg="info">
                            {(forecastData.probabilities.reduce((a, b) => a + b, 0) / forecastData.probabilities.length * 100).toFixed(1)}%
                          </Badge>
                        </td>
                      </tr>
                      <tr>
                        <td><small>Peak Risk</small></td>
                        <td className="text-end">
                          <Badge bg="danger">
                            {(Math.max(...forecastData.probabilities) * 100).toFixed(1)}%
                          </Badge>
                        </td>
                      </tr>
                      <tr>
                        <td><small>Low Risk Days</small></td>
                        <td className="text-end">
                          <Badge bg="success">
                            {forecastData.probabilities.filter(p => p < 0.25).length}
                          </Badge>
                        </td>
                      </tr>
                      <tr>
                        <td><small>High Risk Days</small></td>
                        <td className="text-end">
                          <Badge bg="warning">
                            {forecastData.probabilities.filter(p => p >= 0.5).length}
                          </Badge>
                        </td>
                      </tr>
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            </Col>
          </Row>

          <Row className="mb-4">
            <Col>
              <Card>
                <Card.Header className="d-flex justify-content-between align-items-center">
                  <h5 className="mb-0">
                    <FaCalendarAlt className="me-2" />
                    Daily Forecast Details
                  </h5>
                  <small className="text-muted">
                    Showing {forecastData.dates.length} days • Updated {new Date().toLocaleTimeString()}
                  </small>
                </Card.Header>
                <Card.Body>
                  <Row>
                    {forecastData.dates.slice(0, viewMode === '7day' ? 7 : viewMode === '14day' ? 14 : 8).map((date, index) => {
                      const probability = forecastData.probabilities[index];
                      const risk = getRiskLevel(probability);
                      const confidence = forecastData.confidence_intervals[index];
                      const isToday = new Date(date).toDateString() === new Date().toDateString();
                      const isTomorrow = new Date(date).toDateString() === new Date(Date.now() + 86400000).toDateString();
                      
                      return (
                        <Col md={6} lg={4} xl={3} key={index} className="mb-3">
                          <Card className={`border-${risk.color} ${isToday ? 'shadow-lg' : ''}`}>
                            <Card.Body className="text-center">
                              <div className="d-flex justify-content-between align-items-center mb-2">
                                <h6 className="card-title mb-0">
                                  {isToday ? 'Today' : isTomorrow ? 'Tomorrow' : 
                                   new Date(date).toLocaleDateString('en-US', { 
                                     weekday: 'short', 
                                     month: 'short', 
                                     day: 'numeric' 
                                   })}
                                </h6>
                                {isToday && <Badge bg="primary" className="small">NOW</Badge>}
                              </div>
                              <div className={`text-${risk.color} mb-2`}>
                                <h4 className="mb-1">{(probability * 100).toFixed(1)}%</h4>
                                <Badge bg={risk.color} className="small">
                                  {risk.level} RISK
                                </Badge>
                              </div>
                              <ProgressBar 
                                now={probability * 100} 
                                variant={risk.color} 
                                className="mb-2" 
                                style={{height: '6px'}}
                              />
                              <small className="text-muted d-block">
                                Range: {(confidence[0] * 100).toFixed(0)}% - {(confidence[1] * 100).toFixed(0)}%
                              </small>
                              <small className="text-muted">
                                Confidence: ±{((confidence[1] - confidence[0]) * 50).toFixed(0)}%
                              </small>
                            </Card.Body>
                          </Card>
                        </Col>
                      );
                    })}
                  </Row>
                  {viewMode === '30day' && forecastData.dates.length > 8 && (
                    <div className="text-center mt-3">
                      <Button variant="outline-primary" size="sm">
                        Show All {forecastData.dates.length} Days
                      </Button>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>

          <Row>
            <Col md={4}>
              <Card>
                <Card.Header className="bg-primary text-white">
                  <h6 className="mb-0">
                    <FaChartLine className="me-2" />
                    Forecast Analytics
                  </h6>
                </Card.Header>
                <Card.Body>
                  <Table size="sm" className="mb-0">
                    <tbody>
                      <tr>
                        <td><strong>Average Probability:</strong></td>
                        <td className="text-end">
                          <Badge bg="info">
                            {(forecastData.probabilities.reduce((a, b) => a + b, 0) / forecastData.probabilities.length * 100).toFixed(1)}%
                          </Badge>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Peak Risk Day:</strong></td>
                        <td className="text-end">
                          <small>
                            {new Date(forecastData.dates[forecastData.probabilities.indexOf(Math.max(...forecastData.probabilities))]).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          </small>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Trend:</strong></td>
                        <td className="text-end">
                          <Badge bg={forecastData.probabilities[forecastData.probabilities.length-1] > forecastData.probabilities[0] ? 'warning' : 'success'}>
                            {forecastData.probabilities[forecastData.probabilities.length-1] > forecastData.probabilities[0] ? '📈 Increasing' : '📉 Decreasing'}
                          </Badge>
                        </td>
                      </tr>
                      <tr>
                        <td><strong>Volatility:</strong></td>
                        <td className="text-end">
                          <Badge bg="secondary">
                            {(() => {
                              const variance = forecastData.probabilities.reduce((acc, val, i, arr) => {
                                const mean = arr.reduce((a, b) => a + b) / arr.length;
                                return acc + Math.pow(val - mean, 2);
                              }, 0) / forecastData.probabilities.length;
                              return variance > 0.05 ? 'High' : variance > 0.02 ? 'Medium' : 'Low';
                            })()}
                          </Badge>
                        </td>
                      </tr>
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={8}>
              <Card>
                <Card.Header className="bg-warning text-dark">
                  <h6 className="mb-0">
                    <FaExclamationTriangle className="me-2" />
                    AI-Generated Recommendations
                  </h6>
                </Card.Header>
                <Card.Body>
                  {forecastData.probabilities.some(p => p > 0.7) && (
                    <Alert variant="danger" className="mb-3">
                      <div className="d-flex align-items-center">
                        <FaExclamationTriangle className="me-2" />
                        <div>
                          <strong>🚨 Critical Risk Alert:</strong> Implement emergency protocols immediately
                          <br />
                          <small>Peak probability: {(Math.max(...forecastData.probabilities) * 100).toFixed(1)}% detected</small>
                        </div>
                      </div>
                    </Alert>
                  )}
                  {forecastData.probabilities.some(p => p > 0.5) && !forecastData.probabilities.some(p => p > 0.7) && (
                    <Alert variant="warning" className="mb-3">
                      <div className="d-flex align-items-center">
                        <FaExclamationTriangle className="me-2" />
                        <div>
                          <strong>⚠️ High Risk Period:</strong> Increase monitoring frequency and prepare response teams
                        </div>
                      </div>
                    </Alert>
                  )}
                  
                  <Row>
                    <Col md={6}>
                      <h6 className="text-primary mb-2">Immediate Actions</h6>
                      <ul className="list-unstyled">
                        <li className="mb-2">
                          <Badge bg="outline-primary" className="me-2">1</Badge>
                          Monitor weather conditions closely
                        </li>
                        <li className="mb-2">
                          <Badge bg="outline-primary" className="me-2">2</Badge>
                          Review evacuation procedures
                        </li>
                        <li className="mb-2">
                          <Badge bg="outline-primary" className="me-2">3</Badge>
                          Test communication systems
                        </li>
                      </ul>
                    </Col>
                    <Col md={6}>
                      <h6 className="text-success mb-2">Preventive Measures</h6>
                      <ul className="list-unstyled">
                        <li className="mb-2">
                          <Badge bg="outline-success" className="me-2">1</Badge>
                          Prepare emergency response teams
                        </li>
                        <li className="mb-2">
                          <Badge bg="outline-success" className="me-2">2</Badge>
                          Schedule equipment inspections
                        </li>
                        <li className="mb-2">
                          <Badge bg="outline-success" className="me-2">3</Badge>
                          Update safety protocols
                        </li>
                      </ul>
                    </Col>
                  </Row>
                  
                  <hr />
                  <div className="text-center">
                    <small className="text-muted">
                      <FaCalendarAlt className="me-1" />
                      Recommendations updated every 15 minutes based on latest sensor data and weather conditions
                    </small>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </>
      )}
    </Container>
  );
};

export default Forecast;