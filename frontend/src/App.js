import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import RiskMap from './components/RiskMap';
import Alerts from './components/Alerts';
import Forecast from './components/Forecast';
import SensorData from './components/SensorData';
import DataSources from './components/DataSources';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container-fluid">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/risk-map" element={<RiskMap />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/sensors" element={<SensorData />} />
            <Route path="/data-sources" element={<DataSources />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;