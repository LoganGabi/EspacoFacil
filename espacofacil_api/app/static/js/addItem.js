document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("equipments");
    const totalForms = document.querySelector("#id_roomequipment_set-TOTAL_FORMS");

    function addForm() {
        let formNum = Number(totalForms.value);
        let newForm = container.children[0].cloneNode(true);
        newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formNum}-`);
        container.appendChild(newForm);
        totalForms.value = formNum + 1;
    }

    let addButton = document.createElement("button");
    addButton.textContent = "Adicionar Equipamento";
    addButton.type = "button";
    addButton.onclick = addForm;
    container.after(addButton);
});