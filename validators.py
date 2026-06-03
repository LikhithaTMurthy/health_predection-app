import re
from datetime import datetime, date
from email_validator import validate_email, EmailNotValidError

class PatientValidator:
    """Validator for patient data"""
    
    @staticmethod
    def validate_full_name(name):
        """Validate full name"""
        if not name or not isinstance(name, str):
            return False, "Full name is required and must be a string"
        
        if len(name.strip()) < 2:
            return False, "Full name must be at least 2 characters long"
        
        if len(name) > 255:
            return False, "Full name must not exceed 255 characters"
        
        return True, "Valid"
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        try:
            valid = validate_email(email)
            return True, "Valid"
        except EmailNotValidError as e:
            return False, f"Invalid email: {str(e)}"
    
    @staticmethod
    def validate_date_of_birth(dob_str):
        """Validate date of birth"""
        try:
            if isinstance(dob_str, date):
                dob = dob_str
            else:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            
            today = date.today()
            
            if dob > today:
                return False, "Date of birth cannot be in the future"
            
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if age < 0:
                return False, "Date of birth is invalid"
            
            if age > 150:
                return False, "Date of birth must be within reasonable range"
            
            return True, "Valid"
        except (ValueError, TypeError):
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    @staticmethod
    def validate_numeric_value(value, field_name, min_val=0, max_val=1000):
        """Validate numeric blood test values"""
        try:
            val = float(value)
            
            if val < min_val or val > max_val:
                return False, f"{field_name} must be between {min_val} and {max_val}"
            
            return True, "Valid"
        except (ValueError, TypeError):
            return False, f"{field_name} must be a valid number"
    
    @staticmethod
    def validate_glucose(glucose):
        """Validate glucose level (mg/dL)"""
        # Normal: 70-100 fasting, but can go higher after meals
        return PatientValidator.validate_numeric_value(glucose, "Glucose", 0, 500)
    
    @staticmethod
    def validate_haemoglobin(haemoglobin):
        """Validate haemoglobin level (g/dL)"""
        # Normal range: 12-17.5 for adults, but we'll allow wider range for flexibility
        return PatientValidator.validate_numeric_value(haemoglobin, "Haemoglobin", 0, 25)
    
    @staticmethod
    def validate_cholesterol(cholesterol):
        """Validate cholesterol level (mg/dL)"""
        # Desirable: <200, Borderline high: 200-239, High: 240+
        return PatientValidator.validate_numeric_value(cholesterol, "Cholesterol", 0, 500)
    
    @staticmethod
    def validate_all(data):
        """Validate all patient data"""
        errors = {}
        
        # Validate full name
        valid, msg = PatientValidator.validate_full_name(data.get('full_name', ''))
        if not valid:
            errors['full_name'] = msg
        
        # Validate email
        valid, msg = PatientValidator.validate_email(data.get('email', ''))
        if not valid:
            errors['email'] = msg
        
        # Validate date of birth
        valid, msg = PatientValidator.validate_date_of_birth(data.get('date_of_birth', ''))
        if not valid:
            errors['date_of_birth'] = msg
        
        # Validate glucose
        valid, msg = PatientValidator.validate_glucose(data.get('glucose', ''))
        if not valid:
            errors['glucose'] = msg
        
        # Validate haemoglobin
        valid, msg = PatientValidator.validate_haemoglobin(data.get('haemoglobin', ''))
        if not valid:
            errors['haemoglobin'] = msg
        
        # Validate cholesterol
        valid, msg = PatientValidator.validate_cholesterol(data.get('cholesterol', ''))
        if not valid:
            errors['cholesterol'] = msg
        
        return len(errors) == 0, errors
