# 🚨 AI-Based Rockfall Prediction and Alert System for Open-Pit Mines

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2+-61DAFB.svg)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

A comprehensive, production-ready AI-powered system that predicts and alerts about potential rockfall incidents in open-pit mines. This system integrates multi-source data inputs, advanced machine learning algorithms, and real-time monitoring to enhance mine safety and operational efficiency.

### 🌟 Key Features

- **🤖 AI-Powered Predictions**: Advanced ML models using Random Forest and Gradient Boosting
- **📊 Multi-Source Data Integration**: DEM, drone imagery, geotechnical sensors, environmental data
- **🗺️ Real-Time Risk Mapping**: Interactive visualization with risk zones and probability heat maps
- **📱 Smart Alert System**: SMS/Email notifications with escalation protocols
- **📈 7-Day Forecasting**: Probability-based predictions with confidence intervals
- **🎛️ User-Friendly Dashboard**: Responsive web interface with real-time monitoring
- **🔧 Sensor Management**: Complete sensor network monitoring and maintenance tracking
- **🐳 Production Ready**: Docker deployment with scalable architecture

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Engine     │
│   (React)       │◄──►│   (Flask)       │◄──►│   (sklearn)     │
│   Port: 3000    │    │   Port: 5000    │    │   Predictions   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │              ┌─────────────────┐              │
         │              │   Database      │              │
         │              │ (SQLite/Postgres)│              │
         │              └─────────────────┘              │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sensor Data   │    │   Alert System  │    │   Risk Maps &   │
│   Simulator     │    │   (SMS/Email)   │    │   Forecasting   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
rockfall-prediction-system/
├── 📱 frontend/                    # React Dashboard
│   ├── src/components/            # UI Components
│   │   ├── Dashboard.js          # Main dashboard
│   │   ├── RiskMap.js            # Interactive risk mapping
│   │   ├── Alerts.js             # Alert management
│   │   ├── Forecast.js           # Prediction forecasting
│   │   └── SensorData.js         # Sensor monitoring
│   └── package.json              # Frontend dependencies
├── 🔧 backend/                     # Flask API Server
│   ├── app.py                    # Main API application
│   ├── models.py                 # Database models
│   └── alert_service.py          # Notification services
├── 🤖 ml_models/                   # Machine Learning
│   └── rockfall_predictor.py     # AI prediction engine
├── 📊 data_processing/             # Data Pipeline
│   └── sensor_simulator.py       # Realistic sensor simulation
├── ⚙️ config/                      # Configuration
│   └── emergency_contacts.json   # Alert contacts
├── 🐳 deployment/                  # Docker & Production
│   ├── docker-compose.yml        # Container orchestration
│   ├── Dockerfile.backend        # Backend container
│   └── Dockerfile.frontend       # Frontend container
├── 📜 scripts/                     # Automation Scripts
│   └── setup.py                  # Automated setup
├── 🚀 run_system.py               # System launcher
├── 📋 requirements.txt            # Python dependencies
└── 📖 Documentation files
```

## ⚡ Quick Start

### 🔥 One-Command Setup
```bash
# 1. Run automated setup
python scripts/setup.py

# 2. Start the complete system with sensor simulation
python run_system.py --with-simulator
```

### 🌐 Access Points
- **📊 Dashboard**: http://localhost:3000
- **🔧 API**: http://localhost:5000  
- **❤️ Health Check**: http://localhost:5000/api/health

## 🛠️ Technology Stack

### Backend
- **🐍 Python 3.8+**: Core language
- **🌶️ Flask**: Web framework
- **🗄️ SQLAlchemy**: Database ORM
- **🤖 scikit-learn**: Machine learning
- **📊 NumPy/Pandas**: Data processing

### Frontend  
- **⚛️ React 18**: UI framework
- **🎨 Bootstrap 5**: Styling
- **🗺️ Leaflet**: Interactive maps
- **📈 Chart.js**: Data visualization
- **📱 Responsive Design**: Mobile-friendly

### Infrastructure
- **🐳 Docker**: Containerization
- **🗄️ PostgreSQL/SQLite**: Database
- **📨 Twilio**: SMS alerts
- **📧 SendGrid**: Email notifications
- **☁️ Production Ready**: Scalable deployment
## 
🎮 System Capabilities

### 🔍 Real-Time Monitoring
- **Live Data Processing**: Continuous sensor data ingestion and analysis
- **Risk Level Assessment**: Automatic classification (LOW/MEDIUM/HIGH/CRITICAL)
- **Interactive Dashboards**: Real-time visualization of mine conditions
- **Sensor Health Monitoring**: Battery levels, connectivity status, maintenance alerts

### 🤖 AI-Powered Predictions
- **Multi-Algorithm Approach**: Random Forest + Gradient Boosting ensemble
- **Feature Engineering**: 8+ input parameters including displacement, strain, weather
- **Confidence Intervals**: Statistical uncertainty quantification
- **Adaptive Learning**: Model retraining with new data

### 🚨 Smart Alert System
- **Multi-Channel Notifications**: SMS, Email, Dashboard alerts
- **Escalation Protocols**: Risk-based contact hierarchy
- **Emergency Scenarios**: Automated response procedures
- **Alert Management**: Acknowledgment, resolution tracking

### 📊 Advanced Analytics
- **7-Day Forecasting**: Probability predictions with confidence bands
- **Risk Mapping**: Spatial visualization of danger zones
- **Historical Analysis**: Trend identification and pattern recognition
- **Performance Metrics**: Model accuracy and system reliability stats

## 🚀 Installation Options

### Option 1: Automated Setup (Recommended)
```bash
git clone <repository-url>
cd rockfall-prediction-system
python scripts/setup.py
python run_system.py --with-simulator
```

### Option 2: Manual Installation
```bash
# Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Configuration
cp .env.example .env
# Edit .env with your settings

# Start services
python run_system.py
```

### Option 3: Docker Deployment
```bash
cd deployment
docker-compose up -d
```

## 📊 Sample Data & Testing

### 🎯 Sensor Simulator
The system includes a realistic sensor simulator that generates:
- **Displacement readings** (0.1-3.0 mm)
- **Strain measurements** (50-200 μstrain)  
- **Pore pressure data** (20-80 kPa)
- **Environmental factors** (rainfall, temperature, vibration)
- **Emergency scenarios** for testing alert systems

### 🧪 Test the System
```bash
# Start sensor simulation
python data_processing/sensor_simulator.py

# Generate emergency scenario
# Choose option 3 in the simulator menu

# Send test API request
curl -X POST http://localhost:5000/api/sensor-data \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "TEST-001",
    "sensor_type": "displacement", 
    "location_x": -23.5505,
    "location_y": -46.6333,
    "value": 2.5,
    "unit": "mm",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

## 🔧 Configuration

### 🌍 Environment Variables (.env)
```bash
# Database Configuration
DATABASE_URL=sqlite:///rockfall_system.db

# Alert System (SMS)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# Alert System (Email)  
SENDGRID_API_KEY=your_sendgrid_key
FROM_EMAIL=alerts@yourmine.com

# Security
SECRET_KEY=your_secret_key_here
```

### 👥 Emergency Contacts
Edit `config/emergency_contacts.json`:
```json
{
  "emergency_contacts": [
    {
      "name": "Mine Safety Manager",
      "phone": "+1234567890", 
      "email": "safety@mine.com",
      "role": "primary"
    }
  ],
  "escalation_rules": {
    "CRITICAL": ["primary", "secondary", "emergency"]
  }
}
```

## 📈 Dashboard Features

### 🎛️ Main Dashboard
- **Risk Level Gauge**: Current probability with color-coded alerts
- **System Status**: Real-time health monitoring of all components
- **Recent Alerts**: Latest warnings and notifications
- **Quick Stats**: Key metrics and performance indicators

### 🗺️ Interactive Risk Map
- **Spatial Visualization**: Risk zones overlaid on mine layout
- **Sensor Locations**: Real-time sensor status and readings
- **Risk Heat Maps**: Probability gradients across mine areas
- **Export Capabilities**: Data export for reporting and analysis

### 📊 Forecasting Dashboard
- **7-Day Predictions**: Probability trends with confidence intervals
- **Risk Calendars**: Daily risk levels and recommendations
- **Weather Integration**: Environmental factor correlations
- **Trend Analysis**: Historical patterns and seasonal variations

### ⚙️ Sensor Management
- **Network Overview**: All sensors with status indicators
- **Battery Monitoring**: Power levels and maintenance schedules
- **Data Quality**: Signal strength and reading reliability
- **Maintenance Tracking**: Service history and upcoming tasks

## 🔒 Security & Production

### 🛡️ Security Features
- **Input Validation**: All API endpoints protected against injection
- **Error Handling**: Graceful failure modes and logging
- **Rate Limiting**: Protection against API abuse (configurable)
- **HTTPS Ready**: SSL/TLS encryption support

### 🏭 Production Deployment
- **Docker Containers**: Scalable microservices architecture
- **Database Options**: SQLite (dev) → PostgreSQL (production)
- **Load Balancing**: Nginx reverse proxy configuration
- **Monitoring**: Health checks and performance metrics
- **Backup Systems**: Automated data backup and recovery

## 📚 Documentation

- **📖 [Installation Guide](INSTALLATION.md)**: Detailed setup instructions
- **🔌 [API Documentation](API_DOCUMENTATION.md)**: Complete API reference
- **🐳 Docker Deployment**: Container orchestration guide
- **🔧 Configuration**: Environment and system settings
- **🧪 Testing**: Unit tests and integration testing

## 🎯 Use Cases & Impact

### 🏗️ Mine Safety Enhancement
- **Proactive Risk Detection**: Prevent accidents before they occur
- **Emergency Response**: Automated alert systems save critical time
- **Personnel Protection**: Keep workers safe from rockfall hazards
- **Equipment Protection**: Prevent costly machinery damage

### 💰 Operational Benefits
- **Reduced Downtime**: Predictive maintenance prevents unexpected failures
- **Cost Savings**: Avoid expensive emergency repairs and cleanup
- **Insurance Benefits**: Demonstrate proactive safety measures
- **Regulatory Compliance**: Meet safety standards and reporting requirements

### 📊 Data-Driven Decisions
- **Historical Analysis**: Learn from past incidents and patterns
- **Optimization**: Improve mining operations based on risk data
- **Planning**: Better scheduling around predicted high-risk periods
- **Reporting**: Automated documentation for stakeholders

## 🤝 Integration & Customization

### 🔌 API Integration
The system provides RESTful APIs for integration with:
- **Existing Mine Management Systems**
- **SCADA and Industrial Control Systems**
- **Third-party Monitoring Platforms**
- **Mobile Applications and Dashboards**

### 🎛️ Customization Options
- **Risk Thresholds**: Adjust alert levels for specific mine conditions
- **Sensor Types**: Add support for additional sensor technologies
- **Alert Channels**: Integrate with existing notification systems
- **Reporting**: Custom report generation and data export

### 🔧 Hardware Integration
- **Sensor Compatibility**: Support for various sensor manufacturers
- **Communication Protocols**: Modbus, LoRaWAN, cellular, WiFi
- **Edge Computing**: Local processing for remote mine sites
- **Redundancy**: Backup systems and failover mechanisms

## 🚀 Getting Started Checklist

- [ ] **Clone the repository**
- [ ] **Run automated setup**: `python scripts/setup.py`
- [ ] **Configure environment**: Edit `.env` file
- [ ] **Set up alerts**: Configure emergency contacts
- [ ] **Start the system**: `python run_system.py --with-simulator`
- [ ] **Access dashboard**: Open http://localhost:3000
- [ ] **Test alerts**: Run emergency simulation
- [ ] **Review documentation**: Read API and installation guides
- [ ] **Plan integration**: Identify sensor connection points
- [ ] **Deploy to production**: Use Docker for scalable deployment

## 📞 Support & Contributing

### 🆘 Getting Help
- **Documentation**: Check installation and API guides
- **Issues**: Report bugs and feature requests
- **Community**: Join discussions and share experiences
- **Professional Support**: Available for enterprise deployments

### 🤝 Contributing
We welcome contributions! Areas where you can help:
- **New Sensor Types**: Add support for additional sensors
- **ML Improvements**: Enhance prediction algorithms
- **UI/UX**: Improve dashboard design and usability
- **Documentation**: Help improve guides and examples
- **Testing**: Add unit tests and integration tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mining Industry Experts**: For domain knowledge and requirements
- **Open Source Community**: For the excellent tools and libraries
- **Safety Professionals**: For guidance on alert systems and protocols
- **Academic Researchers**: For machine learning and geological insights

---

**⚠️ Safety Notice**: This system is designed to assist in rockfall prediction but should not be the sole basis for safety decisions. Always follow established safety protocols and consult with qualified professionals.