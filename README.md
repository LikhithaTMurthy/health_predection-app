# Health Prediction Application

A comprehensive web-based health prediction application built with Python (Flask) and Bootstrap, designed for managing patient health records and providing AI-powered health risk assessments based on blood test results.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Health Prediction Algorithm](#health-prediction-algorithm)
- [Security Considerations](#security-considerations)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality

- **👥 Patient Management**: Complete CRUD operations for patient records
- **📊 Blood Test Data Storage**: Track glucose, haemoglobin, and cholesterol levels
- **🤖 AI Health Predictions**: Automated health risk assessment based on blood test values
- **💾 Persistent Storage**: SQLite database for reliable data persistence
- **🎨 User-Friendly Interface**: Clean, responsive Bootstrap-based UI
- **✅ Data Validation**: Comprehensive input validation for all patient data
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### Patient Data Management

- Full Name
- Date of Birth (with validation)
- Email Address (unique constraint)
- Glucose Level (mg/dL)
- Haemoglobin Level (g/dL)
- Cholesterol Level (mg/dL)
- Health Assessment Remarks (AI-generated)
- Timestamp tracking (created_at, updated_at)

## 🛠 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework
- **Flask-SQLAlchemy 3.0.5**: ORM for database operations
- **Flask-CORS 4.0.0**: Cross-Origin Resource Sharing support

### Frontend
- **Bootstrap 5.3**: Responsive UI framework
- **HTML5**: Markup
- **CSS3**: Styling
- **JavaScript**: Client-side interactivity

### Database
- **SQLite**: Lightweight, file-based database

### Tools & Libraries
- **python-dotenv**: Environment variable management
- **email-validator**: Email validation
- **Requests**: HTTP library for API calls

## 📦 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/health_predection-app.git
cd health_predection-app
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Do NOT add sensitive information (use defaults for development)
```

### 5. Initialize Database

```bash
# Database will be created automatically on first run
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///patients.db
HEALTH_API_KEY=your-api-key-if-using-external-api
HEALTH_API_ENDPOINT=https://api.example.com/health
```

### Important Security Notes

- **NEVER** commit `.env` file with real credentials
- Change `SECRET_KEY` in production
- Use environment-specific configurations
- Enable HTTPS in production
- Implement proper authentication for production use

## 💻 Usage

### Adding a New Patient

1. Click "Add Patient" button on the home page
2. Fill in all required fields:
   - Full Name (2-255 characters)
   - Email (valid email format, unique)
   - Date of Birth (cannot be future date)
   - Glucose, Haemoglobin, Cholesterol (numeric values)
3. Submit the form
4. Health prediction will be automatically generated
5. Patient record will be saved to database

### Viewing Patient Records

1. Home page displays all patient records in a table
2. Click "View" button to see detailed information
3. Patient details include:
   - Personal information
   - Blood test results with status indicators
   - AI-generated health assessment

### Editing Patient Records

1. Click "Edit" button on patient row or details page
2. Modify any patient information
3. Blood test values will trigger new health assessment
4. Submit to save changes

### Deleting Patient Records

1. Click "Delete" button (trash icon)
2. Confirm the deletion action
3. Record will be permanently removed from database

## 📡 API Endpoints

The application provides RESTful API endpoints:

### Patient Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients` | Get all patients |
| GET | `/api/patients/<id>` | Get specific patient |
| POST | `/api/patients` | Create new patient |
| PUT | `/api/patients/<id>` | Update patient |
| DELETE | `/api/patients/<id>` | Delete patient |

### Example API Usage

```bash
# Get all patients
curl http://localhost:5000/api/patients

# Create new patient
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "date_of_birth": "1990-01-15",
    "email": "john@example.com",
    "glucose": 95,
    "haemoglobin": 14.5,
    "cholesterol": 180
  }'

# Update patient
curl -X PUT http://localhost:5000/api/patients/1 \
  -H "Content-Type: application/json" \
  -d '{"glucose": 100, ...}'

# Delete patient
curl -X DELETE http://localhost:5000/api/patients/1
```

## 🗄️ Database Schema

### Patients Table

```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    glucose FLOAT NOT NULL,
    haemoglobin FLOAT NOT NULL,
    cholesterol FLOAT NOT NULL,
    remarks TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 📁 Project Structure

```
health_predection-app/
├── app.py                 # Flask application entry point
├── models.py             # Database models
├── config.py             # Configuration management
├── validators.py         # Input validation logic
├── health_api.py         # Health prediction service
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── README.md             # This file
│
├── templates/            # Flask templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page with patient list
│   ├── add_patient.html # Add patient form
│   ├── edit_patient.html # Edit patient form
│   ├── view_patient.html # Patient details view
│   ├── 404.html         # Error page
│   └── 500.html         # Error page
│
└── static/              # Static files
    ├── css/
    │   └── style.css    # Custom CSS styles
    └── js/
        └── script.js    # Client-side JavaScript
```

## 🧠 Health Prediction Algorithm

The application uses an evidence-based algorithmic approach to assess health risks:

### Glucose Assessment
- **Normal (70-100 mg/dL)**: ✓ Green status
- **Elevated (100-125 mg/dL)**: ⚠️ Yellow - Prediabetes warning
- **High (>125 mg/dL)**: 🔴 Red - Diabetes risk
- **Low (<70 mg/dL)**: ⚠️ Yellow - Hypoglycemia risk

### Haemoglobin Assessment
- **Low (<12 g/dL)**: ⚠️ Yellow - Anemia indication
- **Normal (12-17.5 g/dL)**: ✓ Green status
- **High (>17.5 g/dL)**: ⚠️ Yellow - Possible dehydration

### Cholesterol Assessment
- **Desirable (<200 mg/dL)**: ✓ Green status
- **Borderline (200-239 mg/dL)**: ⚠️ Yellow - Lifestyle changes needed
- **High (≥240 mg/dL)**: 🔴 Red - Heart disease risk

### Overall Risk Calculation
- Risk count ≥ 2: High risk status 🔴
- Warning count ≥ 3: Moderate risk status ⚠️
- All normal: Healthy status ✓

## 🔒 Security Considerations

### Implemented Security Measures
- ✅ Input validation for all fields
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Email validation and uniqueness
- ✅ CORS configuration
- ✅ Environment variable protection

### Production Recommendations
- 🔐 Enable HTTPS/SSL
- 🔐 Implement user authentication
- 🔐 Add database encryption
- 🔐 Use strong SECRET_KEY
- 🔐 Enable CSRF protection
- 🔐 Implement rate limiting
- 🔐 Add comprehensive logging
- 🔐 Regular security audits

### Before Uploading to GitHub

**IMPORTANT**: Remove all sensitive data before pushing to GitHub:

```bash
# Remove environment file with credentials
rm .env

# Never commit database files
rm *.db

# Clean cache files
rm -rf __pycache__/
rm -rf .pytest_cache/

# Verify sensitive files are not included
git status
git diff --cached --name-only
```

## ⚖️ Disclaimer

**IMPORTANT MEDICAL DISCLAIMER**: This application is developed for **educational purposes only**. 

- The health predictions and assessments are based on simplified algorithms
- **NOT** a substitute for professional medical diagnosis
- **NOT** intended to diagnose, treat, cure, or prevent any disease
- Always consult qualified healthcare professionals for medical advice
- Blood test results should be interpreted by medical professionals
- The application is not FDA approved or medically validated

Users are solely responsible for their health decisions and must seek professional medical consultation for any health concerns.

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🆘 Support & Troubleshooting

### Common Issues

**Issue**: Database not found
```bash
# Solution: Reinitialize database
rm patients.db
python app.py
```

**Issue**: Port 5000 already in use
```bash
# Solution: Use different port
python app.py  # or configure PORT in .env
```

**Issue**: Module import errors
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 📞 Contact

For questions, issues, or suggestions, please:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: ✅ Production Ready (for Educational Use)
