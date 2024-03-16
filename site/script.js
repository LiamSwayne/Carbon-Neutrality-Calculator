// Scalar for slider value adjustment
const sliderScalar = 1.01157945426;

// Toggle organization slider
function toggleOrganization(organizationId) {
    // Get checkbox and slider elements
    const checkbox = document.getElementById(organizationId + 'Checkbox');
    const slider = document.getElementById(organizationId);
    const isChecked = checkbox.checked;
    // Disable slider if checkbox is not checked
    slider.disabled = !isChecked;
    // Reset slider value and update organization quantity
    slider.value = 0;
    updateOrganizationQuantity(organizationId, organizationId + 'Output');
    // Recalculate results
    calculateResults();
}

// Update organization quantity output
function updateOrganizationQuantity(sliderId, outputId) {
    // Get slider and output elements
    const slider = document.getElementById(sliderId);
    const output = document.getElementById(outputId);
    // Calculate slider value and update output text
    const sliderValue = Math.round(Math.pow(sliderScalar, slider.value));
    output.textContent = `${sliderValue - 1} Trees`;
    // Recalculate results
    calculateResults();
}

// Calculate and update results
function calculateResults() {
    // Get CO2 input value or default to 0
    const co2Input = parseFloat(document.getElementById('co2Input').value) || 0;
    let totalCO2Reduction = 0;
    let totalPrice = 0;

    // Loop through organizations
    for (let i = 1; i <= 3; i++) {
        const organizationId = 'organization' + i;
        // Get organization quantity, CO2 absorption rate, and price
        const organizationQuantity = parseInt(document.getElementById(organizationId + 'Output').textContent.split(" ")[0]) || 0;
        const organizationCO2Absorption = i * 5; // Replace with actual CO2 absorption rate
        const organizationPrice = getPricePerOrganization(organizationId);
        // Update total CO2 reduction and price
        totalCO2Reduction += organizationQuantity * organizationCO2Absorption;
        totalPrice += organizationQuantity * organizationPrice;
    }

    // Update result elements
    const resultCO2 = document.getElementById('resultCO2');
    const totalPriceOutput = document.getElementById('totalPrice');
    resultCO2.textContent = `${co2Input - totalCO2Reduction} tons`;
    totalPriceOutput.textContent = `$${totalPrice}`;
}

// Event listener for organization sliders
for (let i = 1; i <= 3; i++) {
    const organizationId = 'organization' + i;
    // Update organization quantity when slider value changes
    document.getElementById(organizationId).addEventListener('input', function () {
        updateOrganizationQuantity(organizationId, organizationId + 'Output');
    });
}

// Event listener for CO2 input
document.getElementById('co2Input').addEventListener('input', calculateResults);

// Event listener for number of trees input
document.getElementById('numberOfTreesInput').addEventListener('input', function () {
    // Get number of trees input value or default to 0
    const numberOfTreesInputValue = parseFloat(this.value) || 0;
    // Get checked organization checkboxes
    const checkedOrganizations = ['organization1Checkbox', 'organization2Checkbox', 'organization3Checkbox'].filter(id => document.getElementById(id).checked);

    // If no organization is checked, check the first one
    if (checkedOrganizations.length === 0) {
        document.getElementById('organization1Checkbox').checked = true;
        toggleOrganization('organization1');
    }

    // Update slider values for checked organizations based on number of trees
    checkedOrganizations.forEach(organizationId => {
        const sliderId = organizationId.replace('Checkbox', '');
        document.getElementById(sliderId).value = Math.log((numberOfTreesInputValue + 1) / checkedOrganizations.length) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

    // Recalculate results
    calculateResults();
});

// Event listener for budget input
document.getElementById('budgetInput').addEventListener('input', function () {
    // Get budget input value or default to 0
    const budgetInputValue = parseFloat(this.value) || 0;
    // Get checked organization checkboxes
    const checkedOrganizations = ['organization1Checkbox', 'organization2Checkbox', 'organization3Checkbox'].filter(id => document.getElementById(id).checked);

    // If no organization is checked, check the first one
    if (checkedOrganizations.length === 0) {
        document.getElementById('organization1Checkbox').checked = true;
        toggleOrganization('organization1');
    }

    // Update slider values for checked organizations based on budget
    checkedOrganizations.forEach(organizationId => {
        const sliderId = organizationId.replace('Checkbox', '');
        const pricePerOrganization = getPricePerOrganization(sliderId);
        const adjustedOrganizationQuantity = Math.floor(budgetInputValue / pricePerOrganization) / checkedOrganizations.length;

        document.getElementById(sliderId).value = Math.log(adjustedOrganizationQuantity + 1) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

    // Recalculate results
    calculateResults();
});

// Function to get the price per organization
function getPricePerOrganization(organizationId) {
    switch (organizationId) {
        case 'organization1':
        case 'organization2':
        case 'organization3':
            return 1; // Assume all organizations have the same price
        default:
            console.error(`Unknown organizationId: ${organizationId}`);
            return 0;
    }
}

// Initial calculations
calculateResults();