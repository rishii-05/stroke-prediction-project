// Real-time form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('strokeForm');
    if (!form) return;
    
    const ageInput = document.getElementById('age');
    const glucoseInput = document.getElementById('avg_glucose_level');
    const bmiInput = document.getElementById('bmi');

    // Validate age
    if (ageInput) {
        ageInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value >= 1 && value <= 120) {
                this.classList.add('valid');
                this.classList.remove('invalid');
            } else if (this.value !== '') {
                this.classList.add('invalid');
                this.classList.remove('valid');
            }
        });
    }

    // Validate glucose
    if (glucoseInput) {
        glucoseInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value >= 50 && value <= 300) {
                this.classList.add('valid');
                this.classList.remove('invalid');
            } else if (this.value !== '') {
                this.classList.add('invalid');
                this.classList.remove('valid');
            }
        });
    }

    // Validate BMI (optional field)
    if (bmiInput) {
        bmiInput.addEventListener('input', function() {
            if (this.value === '') {
                // Empty is valid (optional field)
                this.classList.remove('valid', 'invalid');
            } else {
                const value = parseFloat(this.value);
                if (value >= 10 && value <= 60) {
                    this.classList.add('valid');
                    this.classList.remove('invalid');
                } else {
                    this.classList.add('invalid');
                    this.classList.remove('valid');
                }
            }
        });
    }

    // Form submission
    form.addEventListener('submit', function(e) {
        const age = parseFloat(ageInput.value);
        const glucose = parseFloat(glucoseInput.value);
        const bmi = bmiInput.value ? parseFloat(bmiInput.value) : null;

        if (age < 1 || age > 120) {
            e.preventDefault();
            alert('⚠️ Please enter a valid age between 1 and 120 years.');
            ageInput.focus();
            return false;
        }

        if (glucose < 50 || glucose > 300) {
            e.preventDefault();
            alert('⚠️ Please enter a valid glucose level between 50 and 300 mg/dL.');
            glucoseInput.focus();
            return false;
        }

        // BMI is optional, only validate if provided
        if (bmi !== null && (bmi < 10 || bmi > 60)) {
            e.preventDefault();
            alert('⚠️ Please enter a valid BMI between 10 and 60, or leave it blank.');
            bmiInput.focus();
            return false;
        }

        // Show loading state
        const submitBtn = form.querySelector('.submit-btn');
        submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
        submitBtn.disabled = true;
    });
});
