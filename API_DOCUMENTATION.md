# API Documentation - Rockfall Prediction System

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API does not require authentication. In production, implement proper authentication and authorization.

## Endpoints

### Health Check
Check if the API is running and healthy.

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Sensor Data

#### Submit Sensor Data
Submit new sensor readings to the system.

**POST** `/sensor-data`

**Request Body:**
```json
{
  "sensor_id": "DS-001",
  "sensor_type": "displacement",
  "location_x": -23.5505,
  "location_y": -46.6333,
  "value": 0.8,
  "unit": "mm",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Response:**
```json
{
  "status": "success",
  "id": 123
}
```

**Sensor Types:**
- `displacement` - Slope displacement (mm)
- `strain` - Rock strain (microstrain)
- `pore_pressure` - Pore water pressure (kPa)
- `temperature` - Temperature (°C)
- `rainfall` - Rainfall rate (mm/h)
- `vibration` - Ground vibration (m/s²)

### Risk Assessment

#### Get Current Risk Assessment
Retrieve the latest AI-generated risk assessment.

**GET** `/risk-assessment`

**Response:**
```json
{
  "risk_level": "HIGH",
  "probability": 0.75,
  "affected_zones": [
    {
      "lat": -23.5505,
      "lng": -46.6333,
      "radius": 50,
      "risk_level": 8
    }
  ],
  "timestamp": "2024-01-01T12:00:00.000Z",
  "recommendations": [
    "Restrict access to affected areas",
    "Increase monitoring frequency",
    "Prepare evacuation procedures"
  ]
}
```

**Risk Levels:**
- `LOW` - 0-25% probability
- `MEDIUM` - 25-50% probability  
- `HIGH` - 50-75% probability
- `CRITICAL` - 75-100% probability

### Risk Map

#### Get Risk Map Data
Retrieve spatial risk data for map visualization.

**GET** `/risk-map`

**Response:**
```json
{
  "risk_zones": [
    {
      "lat": -23.5505,
      "lng": -46.6333,
      "risk_value": 0.65,
      "risk_level": "HIGH"
    }
  ],
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### Alerts

#### Get Alerts
Retrieve recent system alerts.

**GET** `/alerts`

**Query Parameters:**
- `limit` (optional) - Maximum number of alerts to return (default: 50)
- `severity` (optional) - Filter by severity level
- `status` (optional) - Filter by alert status

**Response:**
```json
{
  "alerts": [
    {
      "id": 1,
      "alert_type": "ROCKFALL_WARNING",
      "severity": "HIGH",
      "message": "High rockfall risk detected. Probability: 75%",
      "location": "[{\"lat\": -23.5505, \"lng\": -46.6333}]",
      "timestamp": "2024-01-01T12:00:00.000Z",
      "status": "ACTIVE"
    }
  ]
}
```

**Alert Types:**
- `ROCKFALL_WARNING` - Rockfall risk detected
- `SENSOR_FAILURE` - Sensor malfunction
- `SYSTEM_TEST` - Test alert
- `MAINTENANCE_REQUIRED` - Equipment maintenance needed

**Alert Statuses:**
- `ACTIVE` - Alert is active and requires attention
- `ACKNOWLEDGED` - Alert has been acknowledged
- `RESOLVED` - Alert has been resolved

### Forecast

#### Get Rockfall Forecast
Retrieve AI-generated probability forecast for the next 7 days.

**GET** `/forecast`

**Response:**
```json
{
  "dates": [
    "2024-01-01T00:00:00.000Z",
    "2024-01-02T00:00:00.000Z"
  ],
  "probabilities": [0.45, 0.52],
  "confidence_intervals": [
    [0.35, 0.55],
    [0.42, 0.62]
  ]
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": "Missing required field: sensor_id"
}
```

### 404 Not Found
```json
{
  "message": "No risk assessment available"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "Database connection failed"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## Data Formats

### Timestamps
All timestamps should be in ISO 8601 format with UTC timezone:
```
2024-01-01T12:00:00.000Z
```

### Coordinates
Coordinates should be in decimal degrees (WGS84):
- Latitude: -90 to 90
- Longitude: -180 to 180

### Sensor Values
Sensor values should be numeric and include appropriate units:
- Displacement: millimeters (mm)
- Strain: microstrain (μstrain)
- Pressure: kilopascals (kPa)
- Temperature: degrees Celsius (°C)
- Rainfall: millimeters per hour (mm/h)
- Vibration: meters per second squared (m/s²)

## Example Usage

### Python
```python
import requests
import json
from datetime import datetime

# Submit sensor data
sensor_data = {
    "sensor_id": "DS-001",
    "sensor_type": "displacement",
    "location_x": -23.5505,
    "location_y": -46.6333,
    "value": 1.2,
    "unit": "mm",
    "timestamp": datetime.utcnow().isoformat() + "Z"
}

response = requests.post(
    "http://localhost:5000/api/sensor-data",
    json=sensor_data,
    headers={"Content-Type": "application/json"}
)

print(response.json())

# Get risk assessment
risk_response = requests.get("http://localhost:5000/api/risk-assessment")
risk_data = risk_response.json()
print(f"Current risk level: {risk_data['risk_level']}")
```

### JavaScript
```javascript
// Submit sensor data
const sensorData = {
  sensor_id: "DS-001",
  sensor_type: "displacement",
  location_x: -23.5505,
  location_y: -46.6333,
  value: 1.2,
  unit: "mm",
  timestamp: new Date().toISOString()
};

fetch("http://localhost:5000/api/sensor-data", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(sensorData)
})
.then(response => response.json())
.then(data => console.log(data));

// Get alerts
fetch("http://localhost:5000/api/alerts")
.then(response => response.json())
.then(data => {
  console.log(`Found ${data.alerts.length} alerts`);
});
```

### cURL
```bash
# Submit sensor data
curl -X POST http://localhost:5000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "DS-001",
    "sensor_type": "displacement",
    "location_x": -23.5505,
    "location_y": -46.6333,
    "value": 1.2,
    "unit": "mm",
    "timestamp": "2024-01-01T12:00:00.000Z"
  }'

# Get risk assessment
curl http://localhost:5000/api/risk-assessment

# Get alerts
curl http://localhost:5000/api/alerts
```

## Webhooks (Future Enhancement)

In future versions, the system will support webhooks for real-time notifications:

```json
{
  "webhook_url": "https://your-system.com/webhook",
  "events": ["high_risk_detected", "sensor_failure"],
  "secret": "your_webhook_secret"
}
```

## Integration Guidelines

### Real Sensor Integration
To integrate with real sensors:

1. **Data Collection**: Set up data collectors that read from your sensors
2. **Data Transformation**: Convert sensor data to the required API format
3. **Batch Processing**: Send data in batches for better performance
4. **Error Handling**: Implement retry logic for failed requests
5. **Monitoring**: Monitor API responses and sensor connectivity

### Third-party Systems
To integrate with existing mine management systems:

1. **API Gateway**: Use an API gateway for authentication and routing
2. **Data Synchronization**: Implement two-way data sync if needed
3. **Alert Integration**: Forward alerts to existing notification systems
4. **Reporting**: Export data for compliance and reporting requirements

## Security Considerations

For production deployment:

1. **Authentication**: Implement API key or OAuth authentication
2. **HTTPS**: Use SSL/TLS encryption for all communications
3. **Input Validation**: Validate all input data thoroughly
4. **Rate Limiting**: Implement rate limiting to prevent abuse
5. **Logging**: Log all API access for security monitoring
6. **Network Security**: Restrict API access to authorized networks only