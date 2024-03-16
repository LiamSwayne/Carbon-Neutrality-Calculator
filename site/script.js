const sliderScalar = 1.01157945426;

function toggleOrganization(orgId) {
    const checkbox = document.getElementById(orgId + 'Checkbox');
    const slider = document.getElementById(orgId);
    const isChecked = checkbox.checked;
    slider.disabled = !isChecked;

    slider.value = 0;
    updateOrganizationQuantity(orgId, orgId + 'Output');
    calculateResults();
}

function updateOrganizationQuantity(sliderId, outputId) {
    const slider = document.getElementById(sliderId);
    const output = document.getElementById(outputId);
    const sliderValue = Math.round(Math.pow(sliderScalar, slider.value));
    output.textContent = `${sliderValue - 1} Trees`;
    calculateResults();
}

function calculateResults() {
    const carbonInput = parseFloat(document.getElementById('carbonInput').value) || 0;
    let totalCarbonReduction = 0;
    let totalPrice = 0;

    for (let i = 1; i <= 3; i++) {
        const orgId = 'org' + i;
        const orgQuantity = parseInt(document.getElementById(orgId + 'Output').textContent.split(" ")[0]) || 0;
        const orgAbsorption = i * 5;
        const orgPrice = getPricePerOrganization(orgId);

        totalCarbonReduction += orgQuantity * orgAbsorption;
        totalPrice += orgQuantity * orgPrice;
    }

    const carbonResult = document.getElementById('carbonResult');
    const totalPriceOutput = document.getElementById('totalPrice');
    carbonResult.textContent = `${carbonInput - totalCarbonReduction} tons`;
    totalPriceOutput.textContent = `$${totalPrice}`;
}

for (let i = 1; i <= 3; i++) {
    const orgId = 'org' + i;
    document.getElementById(orgId).addEventListener('input', function () {
        updateOrganizationQuantity(orgId, orgId + 'Output');
    });
}

document.getElementById('carbonInput').addEventListener('input', calculateResults);

document.getElementById('numberOfTreesInput').addEventListener('input', function () {
    const treeNumberInputValue = parseFloat(this.value) || 0;
    const checkedOrgs = ['org1Checkbox', 'org2Checkbox', 'org3Checkbox'].filter(id => document.getElementById(id).checked);

    if (checkedOrgs.length === 0) {
        document.getElementById('org1Checkbox').checked = true;
        toggleOrganization('org1');
    }

    checkedOrgs.forEach(orgId => {
        const sliderId = orgId.replace('Checkbox', '');
        document.getElementById(sliderId).value = Math.log((treeNumberInputValue + 1) / checkedOrgs.length) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

    calculateResults();
});

document.getElementById('budgetInput').addEventListener('input', function () {
    const budgetInputValue = parseFloat(this.value) || 0;
    const checkedOrgs = ['org1Checkbox', 'org2Checkbox', 'org3Checkbox'].filter(id => document.getElementById(id).checked);

    if (checkedOrgs.length === 0) {
        document.getElementById('org1Checkbox').checked = true;
        toggleOrganization('org1');
    }

    checkedOrgs.forEach(orgId => {
        const sliderId = orgId.replace('Checkbox', '');
        const pricePerOrg = getPricePerOrganization(sliderId);

        const adjustedOrgQuantity = Math.floor(budgetInputValue / pricePerOrg) / checkedOrgs.length;
        document.getElementById(sliderId).value = Math.log(adjustedOrgQuantity + 1) / Math.log(sliderScalar);
        updateOrganizationQuantity(sliderId, sliderId + 'Output');
    });

    calculateResults();
});

function getPricePerOrganization(orgId) {
    switch (orgId) {
        case 'org1':
        case 'org2':
        case 'org3':
            return 1;
        default:
            console.error(`Unknown organizationId: ${orgId}`);
            return 0;
    }
}

calculateResults();
