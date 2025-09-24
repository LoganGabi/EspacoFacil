// Variável global para armazenar a data selecionada
let dataFormatada;

// Seletores de elementos do DOM
const room = document.getElementById("container");
const idRoom = room.dataset.idroom;
const csrfToken = document.querySelector('[name=csrf-token]').content;

const time_start = document.getElementById("time_start");
const time_end = document.getElementById("time_end");
const occupantRoom = document.getElementById('occupantRoom');

// Seletores para o Modal
const modalOverlay = document.getElementById('schedule-modal');
const modalDateTitle = document.getElementById('modal-date-title');
const closeButton = document.querySelector('.close-button');

// Função para abrir o modal
function openModal() {
    modalOverlay.style.display = 'flex';
}

// Função para fechar o modal
function closeModal() {
    modalOverlay.style.display = 'none';
}

// Event Listeners para fechar o modal
closeButton.addEventListener('click', closeModal);
modalOverlay.addEventListener('click', (event) => {
    // Fecha o modal apenas se o clique for no fundo (overlay)
    if (event.target === modalOverlay) {
        closeModal();
    }
});
console.log("iiiiiiiiiii");
// Função que cria a lista de horários agendados (semelhante à sua original)
function createTime(list, result) {
    let div = document.createElement("div");
    div.style.marginBottom = "10px"; // Adiciona um espaçamento

    let tr = document.createElement("tr");

    let td1 = document.createElement("td");
    td1.classList.add("tds");
    let td2 = document.createElement("td");
    td2.classList.add("tds");
    let td3 = document.createElement("td");
    td3.classList.add("tds");
    let td4 = document.createElement("td");
    td4.classList.add("tds");
    let div_td4 = document.createElement("div");
    div_td4.classList.add("row");
    div_td4.classList.add("justify-content-start");
    let i_edit = document.createElement("i");
    i_edit.className = "fa-regular fa-pen-to-square"; // Classe do ícone de lápis do Bootstrap Icons
    let i_delete = document.createElement("i");
    i_delete.className = "fa-solid fa-trash"; // Classe do ícone de lixeira do Bootstrap Icons

    let idOccupant = document.createElement("input");
    idOccupant.type = "hidden";
    idOccupant.value = result.id;

    let new_occupant = document.createElement("p");
    new_occupant.textContent = result.occupant || "Desocupado"; // Operador || para simplificar
    new_occupant.classList.add("td-novo-horario");
    new_occupant.readOnly = true;

    let new_time_start = document.createElement("p");
    new_time_start.textContent = result.time_start;
    new_time_start.classList.add("td-novo-horario");
    new_time_start.readOnly = true;

    let new_time_end = document.createElement("p");
    new_time_end.textContent = result.time_end;
    new_time_end.classList.add("td-novo-horario");
    new_time_end.readOnly = true;

    if(result.occupant == null){
      new_occupant.value = "Desocupado"
    }
    new_occupant.readOnly = true;

    let form = document.createElement("form");
    form.action = `OccupancyDelete/${result.id}`;
    form.method = "POST";

    let csrf = document.createElement("input");
    csrf.type = "hidden";
    csrf.name = "csrfmiddlewaretoken";
    csrf.value = document.querySelector("[name=csrfmiddlewaretoken]").value;
    form.appendChild(csrf);

    let edit_button = document.createElement("button");
    let col_edit = document.createElement("div");
    col_edit.className = "col-auto";
    edit_button.id = `edit-button-${result.id}`;
    edit_button.textContent = "Editar Horário";
    edit_button.value = result.id;
    edit_button.className = "btn btn-primary btn-edit-form";

    edit_button.appendChild(i_edit);
    
    edit_button.onclick  = () => edit(edit_button);

    // Guarda a URL como atributo data
    const baseUrl = window.location.origin; // ex: http://localhost:8000
    edit_button.dataset.action = `${baseUrl}/OccupancyUpdate/${result.id}`;

    // edit_button.dataset.action = `OccupancyUpdate/${result.id}`;

    let delete_button = document.createElement("button");
    let col_delete = document.createElement("div");
    col_delete.className = "col-auto";
    delete_button.id = `delete-button-${result.id}`;
    delete_button.textContent = "Deletar Horário";
    delete_button.className = "btn btn-danger btn-edit-form";
    delete_button.value = result.id;

    delete_button.appendChild(i_delete);
    form.appendChild(delete_button);

    delete_button.onclick = (event)=>{
      event.preventDefault();
      removeTime(event.target,dataFormatada);
    }
    // Lembre-se que as funções removeTime e edit precisam estar aqui também.
    list.appendChild(tr); 

    tr.appendChild(idOccupant);
    
    tr.appendChild(td1);
    td1.appendChild(new_occupant);

    tr.appendChild(td2);
    td2.appendChild(new_time_start);

    tr.appendChild(td3);
    td3.appendChild(new_time_end);

    tr.appendChild(td4);
        td4.appendChild(div_td4);
            div_td4.appendChild(col_edit);
                col_edit.appendChild(edit_button);
            div_td4.appendChild(col_delete);
                col_delete.appendChild(delete_button);
}

// Função para atualizar a lista de horários no modal
function updateScheduleList(results) {
    console.log(results,'talvz')
    const listContainer = document.getElementById("list");
    // Limpa a lista anterior
    listContainer.innerHTML = '';
    
    if (results.length > 0) {
        results.forEach(result => {
            createTime(listContainer, result);
        });
    } else {
        listContainer.textContent = "Nenhum horário agendado para esta data.";
    }
}

function removeTime(button) {
    // Adiciona uma confirmação para o usuário
    if (!confirm("Tem certeza que deseja deletar este horário?")) {
        return; 
    }

    fetch(`/OccupancyDelete/${button.value}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            day: dataFormatada // Envia o dia para o backend saber qual lista retornar
        })
    })
    .then(response => {
        if (!response.ok) {
            alert("Ocorreu um erro ao deletar o horário.");
            throw new Error('Erro na resposta do servidor');
        }
        return response.json();
    })
    .then(results => {
        // A CORREÇÃO ESTÁ AQUI:
        // Simplesmente chame a função que já sabe como atualizar a lista.
        // Ela vai limpar a lista antiga e recriar com os novos dados.
        if(results.success){
             updateScheduleList(results.data);
        }
        else{
            alert(`${results.message}`)
        }
       
    })
    .catch(error => console.error('Erro ao deletar:', error));
}

// Configuração do Flatpickr
flatpickr("#calendar", {
    inline: true, // Mantém o calendário sempre visível na página
    dateFormat: "Y-m-d",
    locale: "pt",
    onChange: function(selectedDates, dateStr, instance) {
        // 1. Guarda a data selecionada
        dataFormatada = dateStr;

        // 2. Atualiza o título do modal
        const friendlyDate = new Date(selectedDates[0]).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
        modalDateTitle.textContent = `Agendamentos para ${friendlyDate}`;
        
        // 3. Busca os agendamentos existentes para essa data
        fetch(`/OccupancyCreate/${idRoom}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                day: dataFormatada
            })
        })
        .then(response => response.json())
        .then(results => {
            // 4. Preenche a lista de horários no modal
            console.log('Data: ',results.data);
            console.log(results);   
            if(results.success){
                updateScheduleList(results.data)
            }
            else{
                alert(results.message)
            }
            // updateScheduleList(results);
            // 5. Abre o modal
            openModal();
        });
    }
});

// Função para adicionar um novo horário (chamada pelo botão no modal)
function addTime() {
    // Verifica se os campos de tempo foram preenchidos
    if (!time_start.value || !time_end.value) {
        alert("Por favor, preencha o horário inicial e final.");
        return;
    }

    fetch(`/OccupancyCreate/${idRoom}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            day: dataFormatada,
            time_start: time_start.value,
            time_end: time_end.value,
            occupant: occupantRoom.value
        })
    })
    .then(response => response.json())
    .then(results => {
        // Atualiza a lista de horários no modal com os novos dados
        // updateScheduleList(results);
            if(results.success){
                updateScheduleList(results.data)
            }
            else{
                alert(results.message)
            }
        // Limpa os campos de input de tempo
        time_start.value = '';
        time_end.value = '';
    });
}
function edit(edit_button){
  const actionUrl = edit_button.dataset.action;

  window.location.href = actionUrl;
}