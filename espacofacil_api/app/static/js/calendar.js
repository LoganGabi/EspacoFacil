document.addEventListener('DOMContentLoaded', function() {
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
    const addScheduleButton = document.getElementById('add-schedule-button');

    // Seletores para a funcionalidade de recorrência
    const recurrentCheckbox = document.getElementById('recurrent-schedule-checkbox');
    const recurrentSection = document.getElementById('recurrent-schedule-section');

    if (recurrentCheckbox) {
        recurrentCheckbox.addEventListener('change', () => {
            if (recurrentCheckbox.checked) {
                recurrentSection.style.display = 'block';
            } else {
                recurrentSection.style.display = 'none';
            }
        });
    }

    if (addScheduleButton) {
        addScheduleButton.addEventListener('click', addTime);
    }

    // Função para abrir o modal
    function openModal() {
        modalOverlay.style.display = 'flex';
    }

    // Função para fechar o modal
    function closeModal() {
        modalOverlay.style.display = 'none';
    }

    function clearForm() {
    // Limpa os campos de agendamento único e recorrente
    occupantRoom.value = '';
    time_start.value = '';
    time_end.value = '';
    
    // Desmarca o switch de recorrência
    recurrentCheckbox.checked = false;
    
    // Esconde a seção de recorrência
    recurrentSection.style.display = 'none';

    // Limpa os checkboxes dos dias da semana
    document.querySelectorAll('input[name="weekday"]:checked').forEach(checkbox => {
        checkbox.checked = false;
    });

    // Limpa os campos de data da recorrência
    document.getElementById('recurrent-start-date').value = '';
    document.getElementById('recurrent-end-date').value = '';
}
    // Event Listeners para fechar o modal
    closeButton.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (event) => {
        if (event.target === modalOverlay) {
            closeModal();
        }
    });

    // Função que cria a lista de horários agendados
    function createTime(list, result) {
        let div = document.createElement("div");
        div.style.marginBottom = "10px";

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
        i_edit.className = "fa-regular fa-pen-to-square";
        let i_delete = document.createElement("i");
        i_delete.className = "fa-solid fa-trash";

        let idOccupant = document.createElement("input");
        idOccupant.type = "hidden";
        idOccupant.value = result.id;

        let new_occupant = document.createElement("p");
        new_occupant.textContent = result.occupant || "Desocupado";
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

        if (result.occupant == null) {
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
        edit_button.onclick = () => edit(edit_button);

        const baseUrl = window.location.origin;
        edit_button.dataset.action = `${baseUrl}/OccupancyUpdate/${result.id}`;

        let delete_button = document.createElement("button");
        let col_delete = document.createElement("div");
        col_delete.className = "col-auto";
        delete_button.id = `delete-button-${result.id}`;
        delete_button.textContent = "Deletar Horário";
        delete_button.className = "btn btn-danger btn-edit-form";
        delete_button.value = result.id;
        delete_button.appendChild(i_delete);
        form.appendChild(delete_button);

        delete_button.onclick = (event) => {
            event.preventDefault();
            removeTime(delete_button);
        }

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
        const listContainer = document.getElementById("list");
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
                day: dataFormatada
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
            if (results.success) {
                updateScheduleList(results.data);
            } else {
                alert(`${results.message}`)
            }
        })
        .catch(error => console.error('Erro ao deletar:', error));
    }

    // Configuração do Flatpickr
    let scheduledDatesData = {}; // Variável para guardar as datas com agendamentos

    const calendar = flatpickr("#calendar", {
        inline: true,
        dateFormat: "Y-m-d",
        locale: "pt",

        // Função chamada para cada dia renderizado
        onDayCreate: function(dObj, dStr, fp, dayElem) {
            const date = dayElem.dateObj.toISOString().slice(0, 10);
            const count = scheduledDatesData[date]; // Pega a contagem para o dia

            if (count) {
                dayElem.classList.add("has-schedule");
                dayElem.title = `${count} agendamento(s) neste dia`; // Adiciona um tooltip

                // Aplica a classe de cor baseada na contagem
                if (count >= 7) {
                    dayElem.classList.add("busy-4");
                } else if (count >= 5) {
                    dayElem.classList.add("busy-3");
                } else if (count >= 3) {
                    dayElem.classList.add("busy-2");
                } else {
                    dayElem.classList.add("busy-1");
                }
            }
        },

        // Funções que disparam a busca de dados
        onMonthChange: function(selectedDates, dateStr, instance) {
            fetchScheduledDates(instance);
        },
        onReady: function(selectedDates, dateStr, instance) {
            fetchScheduledDates(instance);
        },

        // Função de clique em um dia (sem alterações)
        onChange: function(selectedDates, dateStr, instance) {
            dataFormatada = dateStr;
            const friendlyDate = new Date(selectedDates[0]).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
            modalDateTitle.textContent = `Agendamentos para ${friendlyDate}`;
            
            fetch(`/OccupancyCreate/${idRoom}/`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
                body: JSON.stringify({ day: dataFormatada })
            })
            .then(response => response.json())
            .then(results => {
                if (results.success) {
                    updateScheduleList(results.data);
                } else {
                    alert(results.message);
                }
                clearForm();
                openModal();
            });
        }
    });

    function fetchScheduledDates(instance) {
        const year = instance.currentYear;
        const month = instance.currentMonth + 1;

        fetch(`/api/scheduled-dates/${idRoom}/${year}/${month}/`)
            .then(response => response.json())
            .then(data => {
                scheduledDatesData = data; // Armazena o objeto { 'data': contagem }
                instance.redraw(); // Força o calendário a se redesenhar
            })
            .catch(error => console.error("Erro ao buscar datas agendadas:", error));
    }

    // Função para adicionar um novo horário
    function addTime() {
    // Validação de horário
    if (!time_start.value || !time_end.value) {
        alert("Por favor, preencha o horário inicial e final.");
        return;
    }

    const isRecurrent = recurrentCheckbox.checked;

    if (isRecurrent) {
        // --- LÓGICA PARA AGENDAMENTO RECORRENTE ---
        const selectedWeekdays = Array.from(document.querySelectorAll('input[name="weekday"]:checked')).map(cb => cb.value);
        const recurrentStartDate = document.getElementById('recurrent-start-date').value;
        const recurrentEndDate = document.getElementById('recurrent-end-date').value;

        // Validação dos campos de recorrência
        if (selectedWeekdays.length === 0 || !recurrentStartDate || !recurrentEndDate) {
            alert("Para agendamentos recorrentes, por favor, selecione os dias da semana e o período de repetição.");
            return;
        }

        const recurrentData = {
            occupant: occupantRoom.value,
            time_start: time_start.value,
            time_end: time_end.value,
            repeat_start_date: recurrentStartDate,
            repeat_end_date: recurrentEndDate,
            weekdays: selectedWeekdays
        };

        fetch(`/OccupancyCreateMultiple/${idRoom}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(recurrentData)
        })
        .then(response => response.json())
        .then(result => {
            if (result.error) {
                alert(`Erro: ${result.error}`);
                return;
            }

            // Monta a mensagem de resumo
            let summaryMessage = `${result.message}\n\n`;
            if (result.successful_bookings && result.successful_bookings.length > 0) {
                summaryMessage += `Agendamentos criados com sucesso: ${result.successful_bookings.length}\n`;
            }
            if (result.failed_bookings && result.failed_bookings.length > 0) {
                summaryMessage += `Falharam por conflito: ${result.failed_bookings.length}\n`;
                summaryMessage += `Datas com conflito: ${result.failed_bookings.join(', ')}\n`;
            }
            
            alert(summaryMessage); // Exibe o resumo para o usuário
            clearForm();
            closeModal(); // Fecha o modal após a operação

        }).catch(error => {
            console.error('Erro ao criar agendamentos recorrentes:', error);
            alert('Ocorreu um erro inesperado. Verifique o console para mais detalhes.');
        });

    } else {
        // --- LÓGICA PARA AGENDAMENTO ÚNICO 
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
            alert(results.message);
            if(results.success){
                updateScheduleList(results.data)
                clearForm();
                fetchScheduledDates(calendar); 
            } else {
                alert(results.message)
            }
            // Limpa os campos de input
            clearForm();
        });
    }
}

    function edit(edit_button) {
        const actionUrl = edit_button.dataset.action;
        window.location.href = actionUrl;
    }
});