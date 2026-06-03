# API Documentation

Complete API reference for the Health Prediction Application.

## 📡 Base URL

```
http://localhost:5000
```

## 🔐 Authentication

Currently, the API does not require authentication. In production, implement:
- JWT tokens
- API keys
- OAuth 2.0

## 📋 Response Format

All API responses follow JSON format:

### Success Response

```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-01-15",
  "email": "john@example.com",
  "glucose": 95,
  "haemoglobin": 14.5,
  "cholesterol": 180,
  "remarks": "✓ Glucose Level: Normal | ...",
  "created_at": "2024-01-15 10:30:00",
  "updated_at": "2024-01-15 10:30:00"
}
```

### Error Response

```json
{
  "error": "Error message describing what went wrong"
}
```

### Validation Error Response

```json
{
  "errors": {
    "email": "Invalid email format",
    "glucose": "Glucose must be between 0 and 500"
  }
}
```

## 🔌 API Endpoints

### 1. Get All Patients

**Endpoint:** `GET /api/patients`

**Description:** Retrieve all patient records

**Query Parameters:** None

**Example Request:**
```bash
curl http://localhost:5000/api/patients
```

**Example Response:**
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "date_of_birth": "1990-01-15",
    "email": "john@example.com",
    "glucose": 95,
    "haemoglobin": 14.5,
    "cholesterol": 180,
    "remarks": "✓ Overall Assessment: Blood test values are within normal range",
    "created_at": "2024-01-15 10:30:00",
    "updated_at": "2024-01-15 10:30:00"
  },
  {
    "id": 2,
    "full_name": "Jane Smith",
    "date_of_birth": "1985-05-20",
    "email": "jane@example.com",
    "glucose": 110,
    "haemoglobin": 15.0,
    "cholesterol": 220,
    "remarks": "⚠️ Overall Assessment: Multiple health concerns detected",
    "created_at": "2024-01-16 14:22:00",
    "updated_at": "2024-01-16 14:22:00"
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Database error

---

### 2. Get Specific Patient

**Endpoint:** `GET /api/patients/<id>`

**Description:** Retrieve a specific patient by ID

**Path Parameters:**
- `id` (integer, required) - Patient ID

**Example Request:**
```bash
curl http://localhost:5000/api/patients/1
```

**Example Response:**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-01-15",
  "email": "john@example.com",
  "glucose": 95,
  "haemoglobin": 14.5,
  "cholesterol": 180,
  "remarks": "✓ Overall Assessment: Blood test values are within normal range",
  "created_at": "2024-01-15 10:30:00",
  "updated_at": "2024-01-15 10:30:00"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Patient not found
- `500 Internal Server Error` - Database error

---

### 3. Create Patient

**Endpoint:** `POST /api/patients`

**Description:** Create a new patient record

**Request Body:** JSON object with patient data

**Required Fields:**
- `full_name` (string, 2-255 characters)
- `date_of_birth` (string, format: YYYY-MM-DD, cannot be future date)
- `email` (string, valid email format, unique)
- `glucose` (number, 0-500)
- `haemoglobin` (number, 0-25)
- `cholesterol` (number, 0-500)

**Example Request:**
```bash
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
```

**Example Success Response:** (201 Created)
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-01-15",
  "email": "john@example.com",
  "glucose": 95,
  "haemoglobin": 14.5,
  "cholesterol": 180,
  "remarks": "✓ Overall Assessment: Blood test values are within normal range",
  "created_at": "2024-01-15 10:30:00",
  "updated_at": "2024-01-15 10:30:00"
}
```

**Example Validation Error Response:** (400 Bad Request)
```json
{
  "errors": {
    "email": "Invalid email format",
    "glucose": "Glucose must be between 0 and 500",
    "date_of_birth": "Date of birth cannot be in the future"
  }
}
```

**Example Duplicate Email Error:** (400 Bad Request)
```json
{
  "error": "Email already exists"
}
```

**Status Codes:**
- `201 Created` - Success
- `400 Bad Request` - Validation error or duplicate email
- `500 Internal Server Error` - Database error

---

### 4. Update Patient

**Endpoint:** `PUT /api/patients/<id>`

**Description:** Update an existing patient record

**Path Parameters:**
- `id` (integer, required) - Patient ID

**Request Body:** JSON object with fields to update

**Optional Fields:**
- `full_name` (string, 2-255 characters)
- `date_of_birth` (string, format: YYYY-MM-DD)
- `email` (string, valid email, unique except for current patient)
- `glucose` (number, 0-500)
- `haemoglobin` (number, 0-25)
- `cholesterol` (number, 0-500)

**Example Request:**
```bash
curl -X PUT http://localhost:5000/api/patients/1 \
  -H "Content-Type: application/json" \
  -d '{
    "glucose": 100,
    "haemoglobin": 15.0,
    "cholesterol": 190
  }'
```

**Example Response:** (200 OK)
```json
{
  "id": 1,
  "full_name": "John Doe",
  "date_of_birth": "1990-01-15",
  "email": "john@example.com",
  "glucose": 100,
  "haemoglobin": 15.0,
  "cholesterol": 190,
  "remarks": "✓ Overall Assessment: Blood test values are within normal range",
  "created_at": "2024-01-15 10:30:00",
  "updated_at": "2024-01-15 10:35:00"
}
```

**Status Codes:**
- `200 OK` - Success
- `400 Bad Request` - Validation error
- `404 Not Found` - Patient not found
- `500 Internal Server Error` - Database error

---

### 5. Delete Patient

**Endpoint:** `DELETE /api/patients/<id>`

**Description:** Delete a patient record

**Path Parameters:**
- `id` (integer, required) - Patient ID

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/api/patients/1
```

**Example Response:** (200 OK)
```json
{
  "message": "Patient deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Patient not found
- `500 Internal Server Error` - Database error

---

## 📊 Data Validation Rules

### Full Name
- **Type:** String
- **Length:** 2-255 characters
- **Required:** Yes
- **Example:** "John Doe"

### Date of Birth
- **Type:** Date (YYYY-MM-DD)
- **Constraints:** 
  - Cannot be future date
  - Must be within reasonable age range (< 150 years)
- **Required:** Yes
- **Example:** "1990-01-15"

### Email
- **Type:** String (Email format)
- **Constraints:** 
  - Must be valid email format
  - Must be unique across all patients
- **Required:** Yes
- **Example:** "john@example.com"

### Glucose
- **Type:** Number (Float)
- **Range:** 0-500 mg/dL
- **Normal Range:** 70-100 (fasting)
- **Required:** Yes
- **Example:** 95

### Haemoglobin
- **Type:** Number (Float)
- **Range:** 0-25 g/dL
- **Normal Range:** 12-17.5 g/dL
- **Required:** Yes
- **Example:** 14.5

### Cholesterol
- **Type:** Number (Float)
- **Range:** 0-500 mg/dL
- **Desirable Range:** <200 mg/dL
- **Required:** Yes
- **Example:** 180

---

## 🎯 Health Prediction Algorithm

When a patient is created or updated, the health prediction API automatically generates remarks based on:

### Blood Test Analysis
1. **Glucose Level Analysis** → Diabetes risk assessment
2. **Haemoglobin Level Analysis** → Anemia risk assessment
3. **Cholesterol Level Analysis** → Heart disease risk assessment

### Risk Categories
- ✓ **Green (Normal):** All values within normal range
- ⚠️ **Yellow (Warning):** 1-2 abnormal values
- 🔴 **Red (High Risk):** 2+ critical values

### Remarks Format

Example output:
```
✓ Glucose Level: Normal | ✓ Haemoglobin Level: Normal | ✓ Cholesterol Level: Desirable | ✓ OVERALL ASSESSMENT: Blood test values are within normal range. Maintain healthy lifestyle.
```

---

## 📋 Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Validation error or invalid data |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

### Common Error Messages

```json
{
  "error": "Full name must be at least 2 characters long"
}
```

```json
{
  "error": "Invalid email format"
}
```

```json
{
  "error": "Date of birth cannot be in the future"
}
```

```json
{
  "error": "Email already exists"
}
```

---

## 🧪 API Testing Examples

### Using cURL

```bash
# Get all patients
curl http://localhost:5000/api/patients

# Create patient
curl -X POST http://localhost:5000/api/patients \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test","date_of_birth":"1990-01-01","email":"test@example.com","glucose":95,"haemoglobin":14.5,"cholesterol":180}'

# Get specific patient
curl http://localhost:5000/api/patients/1

# Update patient
curl -X PUT http://localhost:5000/api/patients/1 \
  -H "Content-Type: application/json" \
  -d '{"glucose":100}'

# Delete patient
curl -X DELETE http://localhost:5000/api/patients/1
```

### Using JavaScript Fetch API

```javascript
// Get all patients
fetch('http://localhost:5000/api/patients')
  .then(response => response.json())
  .then(data => console.log(data));

// Create patient
fetch('http://localhost:5000/api/patients', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    full_name: 'John Doe',
    date_of_birth: '1990-01-15',
    email: 'john@example.com',
    glucose: 95,
    haemoglobin: 14.5,
    cholesterol: 180
  })
})
.then(response => response.json())
.then(data => console.log(data));

// Update patient
fetch('http://localhost:5000/api/patients/1', {
  method: 'PUT',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({glucose: 100})
})
.then(response => response.json())
.then(data => console.log(data));

// Delete patient
fetch('http://localhost:5000/api/patients/1', {
  method: 'DELETE'
})
.then(response => response.json())
.then(data => console.log(data));
```

### Using Python Requests

```python
import requests

BASE_URL = 'http://localhost:5000/api/patients'

# Get all patients
response = requests.get(BASE_URL)
print(response.json())

# Create patient
data = {
    'full_name': 'John Doe',
    'date_of_birth': '1990-01-15',
    'email': 'john@example.com',
    'glucose': 95,
    'haemoglobin': 14.5,
    'cholesterol': 180
}
response = requests.post(BASE_URL, json=data)
print(response.json())

# Get specific patient
response = requests.get(f'{BASE_URL}/1')
print(response.json())

# Update patient
data = {'glucose': 100}
response = requests.put(f'{BASE_URL}/1', json=data)
print(response.json())

# Delete patient
response = requests.delete(f'{BASE_URL}/1')
print(response.json())
```

---

## 🔄 Rate Limiting

*Future Enhancement: Implement rate limiting to prevent API abuse*

Recommended limits:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## 📜 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial API release |

---

**API Documentation Version**: 1.0  
**Last Updated**: 2024  
**Status**: Active
