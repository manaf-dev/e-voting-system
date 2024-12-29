let number = document.getElementById("number")
let amount = document.getElementById("amount")
let numberRegex = /^(02[45769]|05[4567]|03[0-2])\d{7}$/
let amountRegex = /^\d+(\.\d{1,2})?$/
let proceed = document.getElementById("proceed")
function validateInputs() {
    try {
        let numberValue = number.value.toString().trim();
        let amountValue = amount.value.toString().trim();

        if (!numberRegex.test(numberValue)) {
            throw new Error("Invalid phone number. Please enter a valid Ghanaian phone number.");
        }

        if (!amountRegex.test(amountValue)) {
            throw new Error("Invalid amount. Please enter a valid numeric value.");
        }

        alert("Validation successful!");
        return true;
    } catch (error) {
        alert(error.message);
        return false;
    }
}

proceed.addEventListener("click", function (e) {
    e.preventDefault();
    validateInputs();
});
