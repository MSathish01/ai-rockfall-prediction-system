from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import uuid
import cv2
import numpy as np
from PIL import Image
import rasterio
from rasterio.features import shapes
from rasterio.warp import calculate_default_transform, reproject, Resampling

data_sources_bp = Blueprint('data_sources', __name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'drone': {'jpg', 'jpeg', 'png', 'tiff', 'tif', 'raw'},
    'dem': {'tif', 'tiff', 'asc', 'xyz', 'hgt'},
    'satellite': {'tif', 'tiff', 'jp2', 'hdf'},
    'geological': {'shp', 'kml', 'gpx', 'geojson', 'json'}
}

def allowed_file(filename, data_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(data_type, set())

class DroneImageAnalyzer:
    """Analyze drone imagery for rockfall risk indicators"""
    
    @staticmethod
    def analyze_rgb_image(image_path):
        """Analyze RGB drone image for visual indicators"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Convert to different color spaces for analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Detect edges (potential cracks/fractures)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze vegetation coverage (green areas)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            vegetation_percentage = (np.sum(green_mask > 0) / green_mask.size) * 100
            
            # Detect potential loose rocks (texture analysis)
            texture_variance = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Rock color analysis (brownish/grayish areas)
            lower_rock = np.array([10, 50, 50])
            upper_rock = np.array([30, 255, 200])
            rock_mask = cv2.inRange(hsv, lower_rock, upper_rock)
            rock_percentage = (np.sum(rock_mask > 0) / rock_mask.size) * 100
            
            # Risk assessment based on analysis
            risk_indicators = []
            if len(contours) > 100:
                risk_indicators.append('high_fracture_density')
            if vegetation_percentage < 10:
                risk_indicators.append('low_vegetation_stability')
            if texture_variance > 1000:
                risk_indicators.append('rough_surface_texture')
            if rock_percentage > 60:
                risk_indicators.append('exposed_rock_face')
            
            return {
                'cracks_detected': len(contours),
                'vegetation_coverage': round(vegetation_percentage, 2),
                'rock_exposure': round(rock_percentage, 2),
                'texture_variance': round(texture_variance, 2),
                'risk_indicators': risk_indicators,
                'overall_risk': 'high' if len(risk_indicators) >= 3 else 'medium' if len(risk_indicators) >= 2 else 'low'
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    @staticmethod
    def analyze_thermal_image(image_path):
        """Analyze thermal drone image for temperature anomalies"""
        try:
            # Load thermal image (assuming it's in a readable format)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                return {"error": "Could not load thermal image"}
            
            # Temperature analysis (assuming pixel values represent temperature)
            mean_temp = np.mean(image)
            std_temp = np.std(image)
            min_temp = np.min(image)
            max_temp = np.max(image)
            
            # Detect hot spots (potential instability indicators)
            threshold = mean_temp + 2 * std_temp
            hot_spots = np.sum(image > threshold)
            
            # Detect cold spots (potential moisture/water infiltration)
            cold_threshold = mean_temp - 2 * std_temp
            cold_spots = np.sum(image < cold_threshold)
            
            return {
                'mean_temperature': round(mean_temp, 2),
                'temperature_variance': round(std_temp, 2),
                'temperature_range': [int(min_temp), int(max_temp)],
                'hot_spots_detected': int(hot_spots),
                'cold_spots_detected': int(cold_spots),
                'thermal_anomalies': hot_spots + cold_spots,
                'risk_level': 'high' if hot_spots > 1000 else 'medium' if hot_spots > 500 else 'low'
            }
            
        except Exception as e:
            return {"error": f"Thermal analysis failed: {str(e)}"}

class DEMAnalyzer:
    """Analyze Digital Elevation Models for slope stability"""
    
    @staticmethod
    def analyze_dem(dem_path):
        """Analyze DEM for slope stability indicators"""
        try:
            with rasterio.open(dem_path) as dataset:
                # Read elevation data
                elevation = dataset.read(1)
                transform = dataset.transform
                
                # Calculate slope
                dy, dx = np.gradient(elevation)
                slope = np.arctan(np.sqrt(dx*dx + dy*dy)) * 180 / np.pi
                
                # Calculate aspect
                aspect = np.arctan2(-dx, dy) * 180 / np.pi
                aspect = np.where(aspect < 0, aspect + 360, aspect)
                
                # Identify steep slopes (potential instability)
                steep_threshold = 45  # degrees
                steep_areas = np.sum(slope > steep_threshold)
                total_pixels = slope.size
                steep_percentage = (steep_areas / total_pixels) * 100
                
                # Calculate roughness (terrain variability)
                roughness = np.std(elevation)
                
                # Identify potential failure zones
                critical_slope = 60  # degrees
                critical_areas = np.sum(slope > critical_slope)
                critical_percentage = (critical_areas / total_pixels) * 100
                
                # Elevation statistics
                elevation_stats = {
                    'min_elevation': float(np.min(elevation)),
                    'max_elevation': float(np.max(elevation)),
                    'mean_elevation': float(np.mean(elevation)),
                    'elevation_range': float(np.max(elevation) - np.min(elevation))
                }
                
                return {
                    'slope_statistics': {
                        'mean_slope': round(float(np.mean(slope)), 2),
                        'max_slope': round(float(np.max(slope)), 2),
                        'steep_areas_percentage': round(steep_percentage, 2)
                    },
                    'elevation_statistics': elevation_stats,
                    'terrain_roughness': round(roughness, 2),
                    'critical_zones_percentage': round(critical_percentage, 2),
                    'stability_assessment': {
                        'risk_level': 'critical' if critical_percentage > 10 else 'high' if steep_percentage > 30 else 'medium' if steep_percentage > 15 else 'low',
                        'failure_potential': 'high' if critical_percentage > 5 else 'medium' if steep_percentage > 25 else 'low'
                    }
                }
                
        except Exception as e:
            return {"error": f"DEM analysis failed: {str(e)}"}

class SatelliteImageAnalyzer:
    """Analyze satellite imagery for large-scale monitoring"""
    
    @staticmethod
    def analyze_satellite_image(image_path):
        """Analyze satellite image for vegetation, moisture, and land cover changes"""
        try:
            with rasterio.open(image_path) as dataset:
                # Read bands (assuming multispectral)
                bands = dataset.read()
                
                if bands.shape[0] >= 4:  # NIR, Red, Green, Blue
                    nir = bands[0].astype(float)
                    red = bands[1].astype(float)
                    green = bands[2].astype(float)
                    blue = bands[3].astype(float)
                    
                    # Calculate NDVI (Normalized Difference Vegetation Index)
                    ndvi = np.divide(nir - red, nir + red, out=np.zeros_like(nir), where=(nir + red) != 0)
                    
                    # Calculate NDWI (Normalized Difference Water Index)
                    ndwi = np.divide(green - nir, green + nir, out=np.zeros_like(green), where=(green + nir) != 0)
                    
                    # Vegetation analysis
                    vegetation_pixels = np.sum(ndvi > 0.3)
                    total_pixels = ndvi.size
                    vegetation_percentage = (vegetation_pixels / total_pixels) * 100
                    
                    # Water/moisture analysis
                    water_pixels = np.sum(ndwi > 0.3)
                    water_percentage = (water_pixels / total_pixels) * 100
                    
                    # Bare soil/rock analysis
                    bare_pixels = np.sum((ndvi < 0.1) & (ndwi < 0.1))
                    bare_percentage = (bare_pixels / total_pixels) * 100
                    
                    return {
                        'vegetation_index': {
                            'mean_ndvi': round(float(np.mean(ndvi)), 3),
                            'vegetation_coverage': round(vegetation_percentage, 2)
                        },
                        'water_index': {
                            'mean_ndwi': round(float(np.mean(ndwi)), 3),
                            'water_coverage': round(water_percentage, 2)
                        },
                        'land_cover': {
                            'vegetation_percent': round(vegetation_percentage, 2),
                            'water_percent': round(water_percentage, 2),
                            'bare_ground_percent': round(bare_percentage, 2)
                        },
                        'stability_indicators': {
                            'vegetation_stability': 'good' if vegetation_percentage > 40 else 'moderate' if vegetation_percentage > 20 else 'poor',
                            'erosion_risk': 'high' if bare_percentage > 60 else 'medium' if bare_percentage > 30 else 'low'
                        }
                    }
                else:
                    # Basic RGB analysis
                    rgb_image = np.transpose(bands[:3], (1, 2, 0))
                    mean_brightness = np.mean(rgb_image)
                    
                    return {
                        'basic_analysis': {
                            'mean_brightness': round(float(mean_brightness), 2),
                            'image_quality': 'good' if mean_brightness > 100 else 'moderate'
                        }
                    }
                    
        except Exception as e:
            return {"error": f"Satellite analysis failed: {str(e)}"}

@data_sources_bp.route('/api/data-sources', methods=['GET'])
def get_data_sources():
    """Get all data sources"""
    try:
        # Mock data for demonstration - in production, this would query a database
        data_sources = {
            'drone': [
                {
                    'id': 1,
                    'filename': 'drone_survey_zone_a_20240115.jpg',
                    'type': 'RGB',
                    'timestamp': datetime.now().isoformat(),
                    'location': {'lat': -23.5505, 'lng': -46.6333},
                    'altitude': 150,
                    'resolution': '4K',
                    'size': '12.5 MB',
                    'status': 'processed',
                    'analysis': {
                        'cracks_detected': 3,
                        'vegetation_coverage': 15.2,
                        'rock_exposure': 68.5,
                        'risk_indicators': ['visible_fractures', 'loose_rocks'],
                        'overall_risk': 'medium'
                    }
                }
            ],
            'dem': [
                {
                    'id': 1,
                    'filename': 'dem_mine_site_2024_v2.tif',
                    'type': 'Digital Elevation Model',
                    'timestamp': datetime.now().isoformat(),
                    'resolution': '1m',
                    'coverage': '500 hectares',
                    'size': '245 MB',
                    'status': 'active',
                    'analysis': {
                        'mean_slope': 42.5,
                        'max_slope': 78.2,
                        'steep_areas_percentage': 25.8,
                        'critical_zones_percentage': 8.3,
                        'stability_assessment': 'high_risk'
                    }
                }
            ],
            'satellite': [
                {
                    'id': 1,
                    'filename': 'sentinel2_20240110.tif',
                    'type': 'Multispectral',
                    'timestamp': datetime.now().isoformat(),
                    'resolution': '10m',
                    'bands': 13,
                    'size': '156 MB',
                    'status': 'processed',
                    'analysis': {
                        'vegetation_coverage': 32.1,
                        'water_coverage': 5.2,
                        'bare_ground_percent': 62.7,
                        'erosion_risk': 'medium'
                    }
                }
            ],
            'geological': [
                {
                    'id': 1,
                    'filename': 'geological_survey_2024.shp',
                    'type': 'Geological Map',
                    'timestamp': datetime.now().isoformat(),
                    'features': 156,
                    'rock_types': ['granite', 'schist', 'quartzite'],
                    'size': '5.2 MB',
                    'status': 'active',
                    'analysis': {
                        'fault_lines': 8,
                        'joint_sets': 3,
                        'weathering_grade': 'moderate',
                        'structural_stability': 'moderate'
                    }
                }
            ]
        }
        
        return jsonify(data_sources)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_sources_bp.route('/api/data-sources/upload', methods=['POST'])
def upload_data_source():
    """Upload and process data source files"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        data_type = request.form.get('type', 'drone')
        location = request.form.get('location', '{}')
        metadata = request.form.get('metadata', '{}')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, data_type):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Create upload directory if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Process the file based on type
        analysis_result = {}
        
        if data_type == 'drone':
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                analysis_result = DroneImageAnalyzer.analyze_rgb_image(file_path)
            elif 'thermal' in filename.lower():
                analysis_result = DroneImageAnalyzer.analyze_thermal_image(file_path)
        
        elif data_type == 'dem':
            if filename.lower().endswith(('.tif', '.tiff')):
                analysis_result = DEMAnalyzer.analyze_dem(file_path)
        
        elif data_type == 'satellite':
            if filename.lower().endswith(('.tif', '.tiff')):
                analysis_result = SatelliteImageAnalyzer.analyze_satellite_image(file_path)
        
        # Create database record (mock for now)
        file_record = {
            'id': str(uuid.uuid4()),
            'filename': filename,
            'unique_filename': unique_filename,
            'type': data_type,
            'file_path': file_path,
            'size': os.path.getsize(file_path),
            'timestamp': datetime.now().isoformat(),
            'location': json.loads(location) if location != '{}' else None,
            'metadata': json.loads(metadata) if metadata != '{}' else None,
            'analysis': analysis_result,
            'status': 'processed' if analysis_result and 'error' not in analysis_result else 'error'
        }
        
        return jsonify({
            'message': 'File uploaded and processed successfully',
            'file_info': file_record
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@data_sources_bp.route('/api/data-sources/<data_type>/<file_id>/analyze', methods=['POST'])
def reanalyze_data_source(data_type, file_id):
    """Re-analyze a specific data source file"""
    try:
        # In production, you would fetch the file info from database
        # For now, return mock analysis
        
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'reanalysis',
            'status': 'completed'
        }
        
        if data_type == 'drone':
            analysis_result.update({
                'cracks_detected': np.random.randint(0, 10),
                'vegetation_coverage': round(np.random.uniform(10, 50), 2),
                'risk_level': np.random.choice(['low', 'medium', 'high'])
            })
        
        return jsonify({
            'message': 'Analysis completed',
            'analysis': analysis_result
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@data_sources_bp.route('/api/data-sources/integration-status', methods=['GET'])
def get_integration_status():
    """Get the status of multi-source data integration"""
    try:
        status = {
            'last_integration': datetime.now().isoformat(),
            'data_sources_count': {
                'drone': 15,
                'dem': 3,
                'satellite': 8,
                'geological': 5,
                'sensors': 12
            },
            'integration_health': 'good',
            'processing_queue': 2,
            'storage_usage': {
                'used_gb': 156.7,
                'total_gb': 500.0,
                'usage_percentage': 31.3
            },
            'recent_activities': [
                {
                    'timestamp': datetime.now().isoformat(),
                    'activity': 'Drone survey processed',
                    'status': 'completed'
                },
                {
                    'timestamp': (datetime.now()).isoformat(),
                    'activity': 'DEM analysis updated',
                    'status': 'completed'
                }
            ]
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500