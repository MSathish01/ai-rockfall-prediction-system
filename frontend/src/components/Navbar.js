import React from 'react';
import { Navbar as BootstrapNavbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaHome, FaMap, FaBell, FaChartLine, FaCog } from 'react-icons/fa';

const Navbar = () => {
  return (
    <BootstrapNavbar bg="dark" variant="dark" expand="lg" sticky="top">
      <Container>
        <BootstrapNavbar.Brand href="/">
          <FaHome className="me-2" />
          Rockfall Prediction System
        </BootstrapNavbar.Brand>
        
        <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">
              <FaHome className="me-1" />
              Dashboard
            </Nav.Link>
            
            <Nav.Link as={Link} to="/risk-map">
              <FaMap className="me-1" />
              Risk Map
            </Nav.Link>
            
            <Nav.Link as={Link} to="/alerts">
              <FaBell className="me-1" />
              Alerts
            </Nav.Link>
            
            <Nav.Link as={Link} to="/forecast">
              <FaChartLine className="me-1" />
              Forecast
            </Nav.Link>
            
            <Nav.Link as={Link} to="/sensors">
              <FaCog className="me-1" />
              Sensors
            </Nav.Link>
          </Nav>
          
          <Nav>
            <Nav.Link className="text-success">
              ● System Online
            </Nav.Link>
          </Nav>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  );
};

export default Navbar;