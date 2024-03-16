const sliderScalar = 1.01157945426;

// Toggle organization slider
function toggleOrganization(organizationId) {
    const checkbox = document.getElementById(organizationId + 'Checkbox');
    const slider = document.getElementById(organizationId);
    const isChecked = checkbox.checked;
    slider.disabled = !isChecked;

    slider.value = 0; // Reset slider value
    updateOrganizationQuantity(organizationId, organizationId + 'Output');
    calculateResults();
}

// Update organization quantity output
function updateOrganizationQuantity(sliderId, outputId) {
    const slider = document.getElementById(sliderId);
    const output = document.getElementById(outputId);
    const sliderValue = Math.round(Math.pow(sliderScalar, slider.value));
    output.textContent = `${sliderValue - 1} Trees`;
    calculateResults();
}

// Calculate and update results
function calculateResults() {
    const co2Input = parseFloat(document.getElementById('co2Input').value) || 0;
    let totalCO2Reduction = 0;
    let totalPrice = 0;

    for (let i = 1; i <= 3; i++) {
        const organizationId = 'organization' + i;
        const organizationQuantity = parseInt(document.getElementById(organizationId + 'Output').textContent.split(" ")[0]) || 0;
        const organizationCO2Absorption = i * 5; // Replace with actual CO2 absorption rate
        const organizationPrice = getPricePerOrganization(organizationId);

        totalCO2Reduction += organizationQuantity * organizationCO2Absorption;
        totalPrice += organizationQuantity * organizationPrice;
    }

    const resultCO2 = document.getElementById('resultCO2');
    const totalPriceOutput = document.getElementById('totalPrice');
    resultCO2.textContent = `${co2Input - totalCO2Reduction} tons`;
    totalPriceOutput.textContent = `$${totalPrice}`;
}

// Event listener for organization sliders
for (let i = 1; i <= 3; i++) {
    const organizationId = 'organization' + i;
    document.getElementById(organizationId).addEventListener('input', function () {
        updateOrganizationQuantity(organizationId, organizationId + 'Output');
    });
}

// Event listener for CO2 input
document.getElementById('co2Input').addEventListener('input', calculateResults);

// Event listener for number of trees input
document.getElementById('numberOfTreesInput').addEventListener('input', function () {
    const numberOfTreesInputValue = parseFloat(this.value) || 0;
    const checkedOrganizations = ['organization1Checkbox', 'organization2Checkbox', 'organization3Checkbox'].filter(id => document.getElementById(id).checked);

    if (checkedOrganizations.length === 0) {
        document.getElementById('organization1Checkbox').checked = true;
        toggleOrganization('organization1');
    }

    checkedOrganizations.forEach(organizationId => {
        const sliderId = organizationId.replace('Checkbox', '');
        document.getElementById(sliderId).value = Math.log((numberOfTreesInputValue + 1) / checkedOrganizations.length) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

    calculateResults();
});

// Update organization quantity based on budget
function updateOrganizationQuantityFromBudget(sliderId, outputId) {
    const slider = document.getElementById(sliderId);
    const output = document.getElementById(outputId);
    const sliderValue = Math.round(Math.pow(sliderScalar, slider.value));
    output.textContent = `${sliderValue - 1} Donations`;
    calculateResults();
}

// Event listener for budget input
document.getElementById('budgetInput').addEventListener('input', function () {
    const budgetInputValue = parseFloat(this.value) || 0;
    const checkedOrganizations = ['organization1Checkbox', 'organization2Checkbox', 'organization3Checkbox'].filter(id => document.getElementById(id).checked);

    if (checkedOrganizations.length === 0) {
        document.getElementById('organization1Checkbox').checked = true;
        toggleOrganization('organization1');
    }

    checkedOrganizations.forEach(organizationId => {
        const sliderId = organizationId.replace('Checkbox', '');
        const pricePerOrganization = getPricePerOrganization(sliderId);
        const adjustedOrganizationQuantity = Math.floor(budgetInputValue / pricePerOrganization) / checkedOrganizations.length;

        document.getElementById(sliderId).value = Math.log(adjustedOrganizationQuantity + 1) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

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