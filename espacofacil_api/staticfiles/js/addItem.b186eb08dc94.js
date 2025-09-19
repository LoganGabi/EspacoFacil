document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("equipments");
    const totalForms = document.querySelector("#id_roomequipment_set-TOTAL_FORMS");

    const containerTimeSlot = document.getElementById("timeslots");
    const totalTimeSlotForms = document.querySelector("#id_roomtimeslot_set-TOTAL_FORMS");

    function addForm() {
        let formNum = Number(totalForms.value);
        let newForm = container.querySelector('.equipment-form-container').cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formNum}-`);
        newForm.querySelectorAll('input').forEach(input => input.value = '');
        container.appendChild(newForm);
        totalForms.value = formNum + 1;
        
        // ✨ Chama a nova função para re-validar dinamicamente
        updateRequiredFields();
    }

    function addTimeSlotForm(){
        let formNum = Number(totalTimeSlotForms.value);
        let newForm = containerTimeSlot.querySelector(".timeslot-form-container").cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formNum}-`);
        newForm.querySelectorAll('input').forEach(input => input.value = '');
        containerTimeSlot.appendChild(newForm);
        totalTimeSlotForms.value = formNum + 1;
    }

    // ✨ Nova função para adicionar 'required' com base na validação
    function updateRequiredFields() {
        const formContainers = document.querySelectorAll('.equipment-form-container');
        formContainers.forEach(formContainer => {
            const equipmentInput = formContainer.querySelector('[id$="-equipment"]');
            const amountInput = formContainer.querySelector('[id$="-amount"]');

            if (equipmentInput && amountInput) {
                // Remove o 'required' do campo 'amount' por padrão
                amountInput.removeAttribute('required');

                // Adiciona 'required' se um equipamento foi selecionado
                if (equipmentInput.value !== "") {
                    amountInput.setAttribute('required', 'required');
                }
            }
        });
    }

    // ✨ Adiciona um listener para o evento 'change' no campo 'equipment'
    container.addEventListener('change', (event) => {
        if (event.target.matches('[id$="-equipment"]')) {
            updateRequiredFields();
        }
    });

    let addButton = document.createElement("button");
    addButton.textContent = "+ Adicionar Equipamento";
    addButton.type = "button";
    addButton.classList.add("btn", "btn-secondary", "mb-3", "btn-sm");
    addButton.onclick = addForm;
    container.after(addButton);

    let addTimeSlotButton = document.createElement("button");
    addTimeSlotButton.textContent = "+ Adicionar Intervalo";
    addTimeSlotButton.type = "button";
    addTimeSlotButton.classList.add("btn", "btn-secondary", "mb-3", "btn-sm");
    addTimeSlotButton.onclick = addTimeSlotForm;
    containerTimeSlot.after(addTimeSlotButton);
    
    // ✨ Chama a função ao carregar a página
    updateRequiredFields();
    console.log("testando")
});