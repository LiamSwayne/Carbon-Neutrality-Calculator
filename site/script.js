const sliderScalar = 1.01157945426;

// Function to toggle organization slider
function toggleOrganization(organizationId) {
    const checkbox = document.getElementById(organizationId + 'Checkbox');
    const slider = document.getElementById(organizationId);
    slider.disabled = !checkbox.checked;

    if (checkbox.checked) {
        // Enable the slider when the checkbox is checked
        slider.value = 0; // Reset the slider value
        updateOrganizationQuantity(organizationId, organizationId + 'Output');
    } else {
        // Disable the slider and update quantity when the checkbox is unchecked
        slider.value = 0;
        updateOrganizationQuantity(organizationId, organizationId + 'Output');
    }

    // Recalculate results
    calculateResults();
}

// Function to update organization quantity output
function updateOrganizationQuantity(sliderId, outputId) {
    const slider = document.getElementById(sliderId);
    const output = document.getElementById(outputId);
    const sliderValue = Math.round(Math.pow(sliderScalar, slider.value));
    output.textContent = `${sliderValue - 1} Donations`;
    calculateResults();
}

// Function to calculate and update results
function calculateResults() {
    const co2Input = parseFloat(document.getElementById('co2Input').value) || 0;
    let totalCO2Reduction = 0;
    let totalPrice = 0;

    // Loop through each organization
    for (let i = 1; i <= 3; i++) {
        const organizationId = 'organization' + i;

        // Get organization quantity
        const organizationQuantity = parseInt(document.getElementById(organizationId + 'Output').textContent.split(" ")[0]) || 0;

        // Get CO2 absorption rate and price from getPricePerOrganization function
        const organizationCO2Absorption = i * 5; // Replace with actual CO2 absorption rate
        const organizationPrice = getPricePerOrganization(organizationId);

        // Update total CO2 reduction and price
        totalCO2Reduction += organizationQuantity * organizationCO2Absorption;
        totalPrice += organizationQuantity * organizationPrice;
    }

    // Update results
    const resultCO2 = document.getElementById('resultCO2');
    const totalPriceOutput = document.getElementById('totalPrice');
    resultCO2.textContent = `${co2Input - totalCO2Reduction} tons`;
    totalPriceOutput.textContent = `$${totalPrice}`;
}

// Event listeners for organization sliders
document.getElementById('organization1').addEventListener('input', function () {
    updateOrganizationQuantity('organization1', 'organization1Output');
});

document.getElementById('organization2').addEventListener('input', function () {
    updateOrganizationQuantity('organization2', 'organization2Output');
});

document.getElementById('organization3').addEventListener('input', function () {
    updateOrganizationQuantity('organization3', 'organization3Output');
});

// Event listener for CO2 input
document.getElementById('co2Input').addEventListener('input', function () {
    calculateResults();
});

// Event listener for number of trees input
document.getElementById('numberOfTreesInput').addEventListener('input', function () {
    const numberOfTreesInputValue = parseFloat(this.value) || 0;

    // Enable at least one organization if none are checked
    const checkedOrganizations = ['organization1Checkbox', 'organization2Checkbox', 'organization3Checkbox'].filter(id => document.getElementById(id).checked);
    if (checkedOrganizations.length === 0) {
        document.getElementById('organization1Checkbox').checked = true;
        toggleOrganization('organization1');
    }

    // Scale up the checked organizations
    checkedOrganizations.forEach(organizationId => {
        const sliderId = organizationId.replace('Checkbox', '');
        document.getElementById(sliderId).value = Math.log((numberOfTreesInputValue + 1) / checkedOrganizations.length) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

    // Recalculate results
    calculateResults();
});

// Function to update organization quantity based on budget
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

    // Enable at least one organization if none are checked
    const checkedOrganizations = ['organization1Checkbox', 'organization2Checkbox', 'organization3Checkbox'].filter(id => document.getElementById(id).checked);
    if (checkedOrganizations.length === 0) {
        document.getElementById('organization1Checkbox').checked = true;
        toggleOrganization('organization1');
    }

    // Calculate the adjusted number of organizations based on budget
    checkedOrganizations.forEach(organizationId => {
        const sliderId = organizationId.replace('Checkbox', '');
        const pricePerOrganization = getPricePerOrganization(sliderId); // Define this function to get the price per organization

        // Adjusted organization quantity based on budget and price per organization and number of organization types enabled
        const adjustedOrganizationQuantity = Math.floor(budgetInputValue / pricePerOrganization) / checkedOrganizations.length;

        // Update the slider and organization quantity output
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
            return 1; // Donation to National Forest Foundation
        case 'organization2':
            return 1; // Donation to #TeamTrees
        case 'organization3':
            return 1; // Donation to One Tree Planted
        default:
            console.error(`Unknown organizationId: ${organizationId}`);
    }
}

// Initial calculations
calculateResults();