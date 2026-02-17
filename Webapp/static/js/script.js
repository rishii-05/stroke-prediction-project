document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("predictionForm");

    form.addEventListener("submit", function(event) {
        let isValid = true;
        const age = document.getElementById("age").value;
        const glucose = document.getElementById("avg_glucose_level").value;
        const bmi = document.getElementById("bmi").value;

        // Function to check if input is a number
        function isNumeric(value) {
            return !isNaN(value) && isFinite(value);
        }

        // Check for empty values
        if (age === "" || glucose === "" || bmi === "") {
            alert("⚠️ All fields are required. Please fill in the missing values.");
            isValid = false;
        }

        // Validate input types
        if (!isNumeric(age) || !isNumeric(glucose) || !isNumeric(bmi)) {
            alert("⚠️ Please enter valid numerical values.");
            isValid = false;
        }

        // Check for valid age range
        if (age < 1 || age > 120) {
            alert("⚠️ Age must be between 1 and 120.");
            isValid = false;
        }

        // Check for valid glucose level
        if (glucose < 50 || glucose > 300) {
            alert("⚠️ Glucose level must be between 50 and 300 mg/dL.");
            isValid = false;
        }

        // Check for valid BMI
        if (bmi < 10 || bmi > 50) {
            alert("⚠️ BMI must be between 10 and 50.");
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault(); // Stop form submission
        }
    });
});
