import os
import logging
import google.generativeai as genai
from datetime import datetime

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class HealthPredictionAPI:
    """Health prediction service using Gemini AI with rule-based fallback"""

    @staticmethod
    def predict_health_condition(patient_data):
        """
        Predict health condition based on blood test values
        using Gemini AI.
        """

        glucose = patient_data.get('glucose', 0)
        haemoglobin = patient_data.get('haemoglobin', 0)
        cholesterol = patient_data.get('cholesterol', 0)

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
You are a healthcare assistant.

Analyze the following blood test values:

Glucose: {glucose} mg/dL
Haemoglobin: {haemoglobin} g/dL
Cholesterol: {cholesterol} mg/dL

Provide:

1. Possible health concerns
2. Overall health assessment
3. Lifestyle recommendations

Keep the response concise (maximum 100 words).

IMPORTANT:
- Do not diagnose diseases.
- Mention that professional medical consultation is recommended.
- Use simple language.
"""

            response = model.generate_content(prompt)

            remarks = response.text.strip()

            return {
                'success': True,
                'remarks': remarks,
                'prediction_date': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")

            # Fallback to local rule-based assessment
            remarks = HealthPredictionAPI._calculate_health_risks(
                glucose,
                haemoglobin,
                cholesterol
            )

            return {
                'success': True,
                'remarks': remarks,
                'prediction_date': datetime.now().isoformat(),
                'fallback': True
            }

    @staticmethod
    def _calculate_health_risks(glucose, haemoglobin, cholesterol):
        """
        Rule-based health risk assessment
        used when Gemini is unavailable.
        """

        risks = []

        # Glucose Assessment
        if glucose < 70:
            risks.append(
                "⚠️ Low Glucose (Hypoglycemia): Consider consulting a doctor"
            )
        elif 70 <= glucose <= 100:
            risks.append(
                "✓ Glucose Level: Normal"
            )
        elif 100 < glucose <= 125:
            risks.append(
                "⚠️ Elevated Glucose: May indicate prediabetes"
            )
        elif glucose > 125:
            risks.append(
                "🔴 High Glucose: Increased diabetes risk"
            )

        # Haemoglobin Assessment
        if haemoglobin < 12:
            risks.append(
                "⚠️ Low Haemoglobin: Possible anemia"
            )
        elif 12 <= haemoglobin <= 17.5:
            risks.append(
                "✓ Haemoglobin Level: Normal"
            )
        elif haemoglobin > 17.5:
            risks.append(
                "⚠️ High Haemoglobin: Possible dehydration or other conditions"
            )

        # Cholesterol Assessment
        if cholesterol < 200:
            risks.append(
                "✓ Cholesterol Level: Desirable"
            )
        elif 200 <= cholesterol < 240:
            risks.append(
                "⚠️ Borderline High Cholesterol"
            )
        elif cholesterol >= 240:
            risks.append(
                "🔴 High Cholesterol: Increased cardiovascular risk"
            )

        risk_count = sum(
            1 for risk in risks if "🔴" in risk
        )

        warning_count = sum(
            1 for risk in risks if "⚠️" in risk
        )

        if risk_count >= 2:
            risks.append(
                "\n⚠️ OVERALL ASSESSMENT: High risk detected. Medical consultation recommended."
            )
        elif warning_count >= 3:
            risks.append(
                "\n⚠️ OVERALL ASSESSMENT: Multiple concerns detected. Consider medical review."
            )
        elif risk_count == 0 and warning_count == 0:
            risks.append(
                "\n✓ OVERALL ASSESSMENT: Values appear within normal ranges."
            )

        return " | ".join(risks)

    @staticmethod
    def get_health_tips(patient_data):
        """
        Generate health tips based on patient values.
        """

        glucose = patient_data.get('glucose', 0)
        cholesterol = patient_data.get('cholesterol', 0)

        tips = []

        if glucose > 100:
            tips.append(
                "- Reduce sugar and refined carbohydrate intake"
            )
            tips.append(
                "- Exercise at least 30 minutes daily"
            )
            tips.append(
                "- Maintain a healthy body weight"
            )

        if cholesterol > 200:
            tips.append(
                "- Increase dietary fiber intake"
            )
            tips.append(
                "- Reduce saturated fat consumption"
            )
            tips.append(
                "- Exercise regularly"
            )

        if not tips:
            tips.append(
                "- Continue your healthy lifestyle"
            )
            tips.append(
                "- Maintain regular exercise"
            )
            tips.append(
                "- Schedule periodic health checkups"
            )

        return tips