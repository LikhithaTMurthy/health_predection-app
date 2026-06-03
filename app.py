import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime, date

from config import config
from models import db, Patient
from validators import PatientValidator
from health_api import HealthPredictionAPI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
CORS(app)

# Create application context
with app.app_context():
    db.create_all()

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    """Display all patients"""
    try:
        patients = Patient.query.all()
        return render_template('index.html', patients=patients)
    except Exception as e:
        logger.error(f"Error loading patients: {str(e)}")
        return render_template('index.html', patients=[], error=str(e))

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    """Add a new patient"""
    if request.method == 'GET':
        return render_template('add_patient.html')
    
    try:
        # Get form data
        data = {
            'full_name': request.form.get('full_name', ''),
            'date_of_birth': request.form.get('date_of_birth', ''),
            'email': request.form.get('email', ''),
            'glucose': request.form.get('glucose', ''),
            'haemoglobin': request.form.get('haemoglobin', ''),
            'cholesterol': request.form.get('cholesterol', '')
        }
        
        # Validate data
        is_valid, errors = PatientValidator.validate_all(data)
        
        if not is_valid:
            return render_template('add_patient.html', errors=errors, data=data), 400
        
        # Check if email already exists
        existing_patient = Patient.query.filter_by(email=data['email']).first()
        if existing_patient:
            errors['email'] = 'Email already exists'
            return render_template('add_patient.html', errors=errors, data=data), 400
        
        # Generate health prediction
        prediction = HealthPredictionAPI.predict_health_condition({
            'glucose': float(data['glucose']),
            'haemoglobin': float(data['haemoglobin']),
            'cholesterol': float(data['cholesterol'])
        })
        
        # Create new patient
        patient = Patient(
            full_name=data['full_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            email=data['email'],
            glucose=float(data['glucose']),
            haemoglobin=float(data['haemoglobin']),
            cholesterol=float(data['cholesterol']),
            remarks=prediction.get('remarks', '')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        logger.info(f"Patient added: {patient.full_name}")
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error adding patient: {str(e)}")
        db.session.rollback()
        return render_template('add_patient.html', error=str(e)), 500

@app.route('/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """Edit patient information"""
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'GET':
        return render_template('edit_patient.html', patient=patient)
    
    try:
        # Get form data
        data = {
            'full_name': request.form.get('full_name', ''),
            'date_of_birth': request.form.get('date_of_birth', ''),
            'email': request.form.get('email', ''),
            'glucose': request.form.get('glucose', ''),
            'haemoglobin': request.form.get('haemoglobin', ''),
            'cholesterol': request.form.get('cholesterol', '')
        }
        
        # Validate data
        is_valid, errors = PatientValidator.validate_all(data)
        
        if not is_valid:
            return render_template('edit_patient.html', patient=patient, errors=errors, data=data), 400
        
        # Check if email already exists (excluding current patient)
        existing_patient = Patient.query.filter_by(email=data['email']).first()
        if existing_patient and existing_patient.id != patient_id:
            errors['email'] = 'Email already exists'
            return render_template('edit_patient.html', patient=patient, errors=errors, data=data), 400
        
        # Generate new health prediction
        prediction = HealthPredictionAPI.predict_health_condition({
            'glucose': float(data['glucose']),
            'haemoglobin': float(data['haemoglobin']),
            'cholesterol': float(data['cholesterol'])
        })
        
        # Update patient
        patient.full_name = data['full_name']
        patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        patient.email = data['email']
        patient.glucose = float(data['glucose'])
        patient.haemoglobin = float(data['haemoglobin'])
        patient.cholesterol = float(data['cholesterol'])
        patient.remarks = prediction.get('remarks', '')
        
        db.session.commit()
        
        logger.info(f"Patient updated: {patient.full_name}")
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error updating patient: {str(e)}")
        db.session.rollback()
        return render_template('edit_patient.html', patient=patient, error=str(e)), 500

@app.route('/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    """Delete a patient"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        patient_name = patient.full_name
        
        db.session.delete(patient)
        db.session.commit()
        
        logger.info(f"Patient deleted: {patient_name}")
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error deleting patient: {str(e)}")
        db.session.rollback()
        return redirect(url_for('index'))

@app.route('/view/<int:patient_id>')
def view_patient(patient_id):
    """View patient details"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        return render_template('view_patient.html', patient=patient)
    except Exception as e:
        logger.error(f"Error viewing patient: {str(e)}")
        return redirect(url_for('index'))

# ============================================================================
# API Routes (JSON)
# ============================================================================

@app.route('/api/patients', methods=['GET'])
def api_get_patients():
    """Get all patients as JSON"""
    try:
        patients = Patient.query.all()
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def api_get_patient(patient_id):
    """Get specific patient as JSON"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        return jsonify(patient.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/patients', methods=['POST'])
def api_create_patient():
    """Create patient via API"""
    try:
        data = request.get_json()
        
        # Validate data
        is_valid, errors = PatientValidator.validate_all(data)
        if not is_valid:
            return jsonify({'errors': errors}), 400
        
        # Check if email exists
        if Patient.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Generate prediction
        prediction = HealthPredictionAPI.predict_health_condition({
            'glucose': float(data['glucose']),
            'haemoglobin': float(data['haemoglobin']),
            'cholesterol': float(data['cholesterol'])
        })
        
        # Create patient
        patient = Patient(
            full_name=data['full_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            email=data['email'],
            glucose=float(data['glucose']),
            haemoglobin=float(data['haemoglobin']),
            cholesterol=float(data['cholesterol']),
            remarks=prediction.get('remarks', '')
        )
        
        db.session.add(patient)
        db.session.commit()
        
        return jsonify(patient.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def api_update_patient(patient_id):
    """Update patient via API"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        data = request.get_json()
        
        # Validate data
        is_valid, errors = PatientValidator.validate_all(data)
        if not is_valid:
            return jsonify({'errors': errors}), 400
        
        # Check email uniqueness
        if Patient.query.filter_by(email=data['email']).first() and patient.email != data['email']:
            return jsonify({'error': 'Email already exists'}), 400
        
        # Generate new prediction
        prediction = HealthPredictionAPI.predict_health_condition({
            'glucose': float(data['glucose']),
            'haemoglobin': float(data['haemoglobin']),
            'cholesterol': float(data['cholesterol'])
        })
        
        # Update patient
        patient.full_name = data['full_name']
        patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        patient.email = data['email']
        patient.glucose = float(data['glucose'])
        patient.haemoglobin = float(data['haemoglobin'])
        patient.cholesterol = float(data['cholesterol'])
        patient.remarks = prediction.get('remarks', '')
        
        db.session.commit()
        
        return jsonify(patient.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def api_delete_patient(patient_id):
    """Delete patient via API"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': 'Patient deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Patient': Patient}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
