// VehiLog Main JavaScript

// Date format handling for dd/mm/yyyy
document.addEventListener('DOMContentLoaded', function() {
    const dateInputs = document.querySelectorAll('input[placeholder="dd/mm/yyyy"]');
    
    dateInputs.forEach(function(input) {
        // Auto-format date input
        input.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2);
            }
            if (value.length >= 5) {
                value = value.substring(0, 5) + '/' + value.substring(5, 9);
            }
            this.value = value;
        });
        
        // Validate date format
        input.addEventListener('blur', function() {
            const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
            const match = this.value.match(dateRegex);
            if (match) {
                const day = parseInt(match[1]);
                const month = parseInt(match[2]);
                const year = parseInt(match[3]);
                
                if (day < 1 || day > 31 || month < 1 || month > 12) {
                    this.style.borderColor = 'red';
                    this.setCustomValidity('Invalid date');
                } else {
                    this.style.borderColor = '';
                    this.setCustomValidity('');
                }
            } else if (this.value) {
                this.style.borderColor = 'red';
                this.setCustomValidity('Invalid date format');
            }
        });
    });
});

// Form validation helpers
function vehiLogValidateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.style.borderColor = 'red';
            isValid = false;
        } else {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// Auto-dismiss alerts
function vehiLogAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.classList.contains('alert-success')) {
                alert.style.opacity = '0';
                setTimeout(function() {
                    alert.remove();
                }, 300);
            }
        }, 3000);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    vehiLogAutoDismissAlerts();
});

// Number formatting for currency
function vehiLogFormatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(amount);
}

// Calculate total expenses
function vehiLogCalculateTotal(expenses) {
    return expenses.reduce((total, expense) => total + parseFloat(expense.amount), 0);
}

// Export functions for global use
window.vehiLog = {
    validateForm: vehiLogValidateForm,
    formatCurrency: vehiLogFormatCurrency,
    calculateTotal: vehiLogCalculateTotal
};