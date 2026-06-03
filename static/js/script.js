// ============================================================================
// Health Prediction App - JavaScript
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// ============================================================================
// Initialization
// ============================================================================

function initializeApp() {
    console.log('Health Prediction App initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize date picker constraints
    initializeDatePickers();
}

// ============================================================================
// Tooltips
// ============================================================================

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ============================================================================
// Form Validation
// ============================================================================

function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// ============================================================================
// Date Picker
// ============================================================================

function initializeDatePickers() {
    const dateOfBirthInputs = document.querySelectorAll('input[name="date_of_birth"]');
    dateOfBirthInputs.forEach(input => {
        input.max = new Date().toISOString().split('T')[0];
    });
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Format date to readable format
 */
function formatDate(dateStr) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateStr).toLocaleDateString(undefined, options);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type}" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    toastContainer.innerHTML = toastHtml;
    document.body.appendChild(toastContainer);
    
    const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
    toast.show();
    
    // Remove container after toast is hidden
    setTimeout(() => toastContainer.remove(), 5500);
}

/**
 * Validate email format
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Format currency
 */
function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

/**
 * API Helper - GET request
 */
async function apiGet(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API GET Error:', error);
        showToast('Error fetching data', 'danger');
        throw error;
    }
}

/**
 * API Helper - POST request
 */
async function apiPost(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API POST Error:', error);
        showToast('Error submitting data', 'danger');
        throw error;
    }
}

/**
 * API Helper - PUT request
 */
async function apiPut(url, data) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API PUT Error:', error);
        showToast('Error updating data', 'danger');
        throw error;
    }
}

/**
 * API Helper - DELETE request
 */
async function apiDelete(url) {
    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API DELETE Error:', error);
        showToast('Error deleting data', 'danger');
        throw error;
    }
}

/**
 * Confirm delete action
 */
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// ============================================================================
// Export functions for global use
// ============================================================================

window.healthApp = {
    formatDate,
    showToast,
    validateEmail,
    formatCurrency,
    apiGet,
    apiPost,
    apiPut,
    apiDelete,
    confirmDelete
};
