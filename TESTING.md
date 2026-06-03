# Testing Guide - Health Prediction Application

## 📋 Manual Testing Checklist

### 1. Application Setup
- [ ] Dependencies installed successfully
- [ ] Environment variables configured (.env created)
- [ ] Database initialized without errors
- [ ] Application starts on port 5000

### 2. Home Page (/)
- [ ] Page loads with correct title
- [ ] Navigation bar displays correctly
- [ ] "Add Patient" button is visible and clickable
- [ ] Patient statistics cards display
- [ ] No patients message displays when database is empty

### 3. Add Patient Feature (/add)
- [ ] Page loads with empty form
- [ ] Form fields are properly labeled
- [ ] All required fields marked with asterisk (*)
- [ ] Reference information displayed correctly

#### Form Validation Testing

| Field | Test Case | Expected Result |
|-------|-----------|-----------------|
| Full Name | Empty | Error: "Full name is required" |
| Full Name | Less than 2 chars | Error: "Must be at least 2 characters" |
| Full Name | Valid name | ✓ Accepted |
| Email | Invalid format | Error: "Invalid email" |
| Email | Valid email | ✓ Accepted |
| Email | Duplicate email | Error: "Email already exists" |
| DOB | Future date | Error: "Cannot be future date" |
| DOB | Valid date | ✓ Accepted |
| Glucose | Non-numeric | Error: "Must be valid number" |
| Glucose | Negative | Error: "Must be between 0-500" |
| Glucose | Valid (95) | ✓ Accepted |
| Haemoglobin | Non-numeric | Error: "Must be valid number" |
| Haemoglobin | Valid (14.5) | ✓ Accepted |
| Cholesterol | Non-numeric | Error: "Must be valid number" |
| Cholesterol | Valid (180) | ✓ Accepted |

### 4. Test Data Sets

#### Valid Patient Records

```
Patient 1: Healthy
- Name: John Healthy
- DOB: 1985-03-15
- Email: john.healthy@test.com
- Glucose: 90 (Normal)
- Haemoglobin: 14.5 (Normal)
- Cholesterol: 180 (Desirable)
Expected: All normal status

Patient 2: Prediabetic
- Name: Jane Prediabetic
- DOB: 1990-06-20
- Email: jane.prediabetic@test.com
- Glucose: 110 (Elevated)
- Haemoglobin: 15.0 (Normal)
- Cholesterol: 220 (Borderline High)
Expected: Warning status

Patient 3: High Risk
- Name: Bob HighRisk
- DOB: 1980-01-10
- Email: bob.highrisk@test.com
- Glucose: 200 (High Diabetes Risk)
- Haemoglobin: 9.5 (Low - Anemia)
- Cholesterol: 280 (High Cholesterol Risk)
Expected: High risk status
```

### 5. CRUD Operations

#### Create ✓
- [ ] Add new patient with valid data
- [ ] Health prediction automatically generated
- [ ] Patient appears in patient list
- [ ] Timestamps recorded correctly

#### Read ✓
- [ ] View patient list on home page
- [ ] Click "View" button to see details
- [ ] All patient information displays correctly
- [ ] Health assessment remarks visible

#### Update ✓
- [ ] Click "Edit" button on patient row
- [ ] Modify patient data
- [ ] Submit changes
- [ ] Updated data appears immediately
- [ ] Updated timestamp changes
- [ ] Health assessment regenerates with new values

#### Delete ✓
- [ ] Click "Delete" button
- [ ] Confirmation dialog appears
- [ ] Confirm deletion
- [ ] Patient removed from list
- [ ] Database reflects deletion

### 6. Patient Details View (/view/<id>)
- [ ] All patient information displays
- [ ] Blood test values shown with color coding
- [ ] Health assessment remarks visible
- [ ] Edit and Delete buttons functional
- [ ] Back to Patients link works

### 7. Responsive Design
- [ ] Desktop view (1920px)
- [ ] Tablet view (768px)
- [ ] Mobile view (375px)
- [ ] Navigation collapses on mobile
- [ ] Tables scroll horizontally on mobile
- [ ] All buttons remain clickable

### 8. Navigation
- [ ] Home logo redirects to /
- [ ] Navigation links work correctly
- [ ] Back buttons navigate properly
- [ ] No broken links

### 9. Error Handling
- [ ] 404 error page displays
- [ ] 500 error page displays
- [ ] Form errors display with styling
- [ ] Validation messages clear and helpful

### 10. Browser Compatibility
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (if available)
- [ ] Mobile browsers

## 🧪 API Testing

### Using curl

```bash
# Get all patients
curl http://localhost:5000/api/patients

# Get specific patient
curl http://localhost:5000/api/patients/1

# Create patient
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test Patient",
    "date_of_birth": "1990-01-01",
    "email": "test@example.com",
    "glucose": 95,
    "haemoglobin": 14.5,
    "cholesterol": 180
  }'

# Update patient
curl -X PUT http://localhost:5000/api/patients/1 \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Name",
    "date_of_birth": "1990-01-01",
    "email": "test@example.com",
    "glucose": 100,
    "haemoglobin": 15.0,
    "cholesterol": 190
  }'

# Delete patient
curl -X DELETE http://localhost:5000/api/patients/1
```

### Using Postman

1. Create new collection "Health App"
2. Import endpoints from API section
3. Create environment variables:
   - `base_url`: http://localhost:5000
4. Run requests and verify responses

## 📊 Performance Testing

### Load Testing
```bash
# Install Apache Bench
# ab -n 100 -c 10 http://localhost:5000/

# Expected: Response time < 500ms for GET requests
```

### Database Performance
- [ ] < 1000 records: Fast retrieval
- [ ] Data integrity maintained
- [ ] No data corruption

## 🔐 Security Testing

- [ ] SQL injection attempts blocked
  ```sql
  email: admin'; DROP TABLE patients;--
  ```
- [ ] XSS attempts sanitized
  ```html
  name: <script>alert('XSS')</script>
  ```
- [ ] CSRF protection enabled
- [ ] No sensitive data in logs
- [ ] Database file protected (permissions)

## 📝 Test Results Template

```markdown
## Test Date: YYYY-MM-DD
## Tester: [Your Name]
## Browser: [Browser/Version]
## OS: [Operating System]

### Results Summary
- Total Tests: X
- Passed: X
- Failed: X
- Skipped: X

### Failed Tests
1. Issue Description
   - Expected: 
   - Actual: 
   - Steps to Reproduce:

### Notes & Observations
- 

### Recommendations
- 
```

## 🐛 Bug Report Template

```markdown
## Bug Title
[Clear, concise title]

## Description
[Detailed description of the issue]

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Screenshots
[Attach if applicable]

## Environment
- OS: 
- Browser: 
- Version: 

## Severity
[ ] Critical  [ ] High  [ ] Medium  [ ] Low
```

## ✅ Pre-Deployment Checklist

- [ ] All tests pass
- [ ] No console errors
- [ ] Database backups created
- [ ] Environment variables configured
- [ ] Security audit complete
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Sensitive data removed
- [ ] Ready for deployment

---

**Testing Version**: 1.0  
**Last Updated**: 2024
