import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthPredictionAPI:
    """Health prediction service using external API"""
    
    @staticmethod
    def predict_health_condition(patient_data):
        """
        Predict health condition based on patient blood test results.
        Uses a free health risk assessment algorithm.
        
        Args:
            patient_data: dict with glucose, haemoglobin, cholesterol
            
        Returns:
            dict with prediction and remarks
        """
        try:
            glucose = patient_data.get('glucose', 0)
            haemoglobin = patient_data.get('haemoglobin', 0)
            cholesterol = patient_data.get('cholesterol', 0)
            
            # Calculate health risks based on blood test values
            remarks = HealthPredictionAPI._calculate_health_risks(
                glucose, haemoglobin, cholesterol
            )
            
            return {
                'success': True,
                'remarks': remarks,
                'prediction_date': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error predicting health condition: {str(e)}")
            return {
                'success': False,
                'remarks': 'Unable to generate health prediction at this time',
                'error': str(e)
            }
    
    @staticmethod
    def _calculate_health_risks(glucose, haemoglobin, cholesterol):
        """
        Calculate health risks based on blood test values.
        This uses a basic algorithmic approach for health risk assessment.
        """
        risks = []
        age = 0  # We can incorporate age if available
        
        # Glucose Assessment
        if glucose < 70:
            risks.append("⚠️ Low Glucose (Hypoglycemia): Consider consulting with doctor")
        elif glucose >= 70 and glucose <= 100:
            risks.append("✓ Glucose Level: Normal")
        elif glucose > 100 and glucose <= 125:
            risks.append("⚠️ Elevated Glucose: Monitor closely, may indicate prediabetes")
        elif glucose > 125:
            risks.append("🔴 High Glucose: Risk of diabetes, immediate medical consultation recommended")
        
        # Haemoglobin Assessment
        if haemoglobin < 12:
            risks.append("⚠️ Low Haemoglobin (Anemia): Consult doctor for iron and B12 levels")
        elif haemoglobin >= 12 and haemoglobin <= 17.5:
            risks.append("✓ Haemoglobin Level: Normal")
        elif haemoglobin > 17.5:
            risks.append("⚠️ High Haemoglobin: May indicate dehydration or blood disorders")
        
        # Cholesterol Assessment
        if cholesterol < 200:
            risks.append("✓ Cholesterol Level: Desirable")
        elif cholesterol >= 200 and cholesterol < 240:
            risks.append("⚠️ Borderline High Cholesterol: Increase physical activity and dietary changes")
        elif cholesterol >= 240:
            risks.append("🔴 High Cholesterol: Risk of heart disease, medication may be needed")
        
        # Combined Risk Assessment
        risk_count = sum(1 for risk in risks if "🔴" in risk)
        warning_count = sum(1 for risk in risks if "⚠️" in risk)
        
        if risk_count >= 2:
            risks.append("\n⚠️ OVERALL ASSESSMENT: High risk detected. Immediate medical consultation strongly recommended.")
        elif warning_count >= 3:
            risks.append("\n⚠️ OVERALL ASSESSMENT: Multiple health concerns detected. Schedule doctor appointment soon.")
        elif risk_count == 0 and warning_count == 0:
            risks.append("\n✓ OVERALL ASSESSMENT: Blood test values are within normal range. Maintain healthy lifestyle.")
        
        return " | ".join(risks)
    
    @staticmethod
    def get_health_tips(patient_data):
        """
        Get personalized health tips based on blood test results.
        """
        glucose = patient_data.get('glucose', 0)
        cholesterol = patient_data.get('cholesterol', 0)
        
        tips = []
        
        if glucose > 100:
            tips.append("- Reduce sugar and refined carbohydrate intake")
            tips.append("- Increase physical activity (at least 30 mins daily)")
            tips.append("- Maintain healthy body weight")
        
        if cholesterol > 200:
            tips.append("- Increase fiber intake (soluble fiber from oats, beans)")
            tips.append("- Reduce saturated fat consumption")
            tips.append("- Exercise regularly")
        
        if not tips:
            tips.append("- Continue current healthy lifestyle")
            tips.append("- Regular exercise and balanced diet")
            tips.append("- Periodic health checkups")
        
        return tips
