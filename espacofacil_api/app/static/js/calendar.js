let dataFormatada;
const room = document.getElementById("container")
const idRoom = room.dataset.idroom;
const csrfToken = document.querySelector('[name=csrf-token]').content;

const time_start = document.getElementById("time_start");
const time_end = document.getElementById("time_end");

const occupant = document.querySelector('select[name="occupants"]');

const occupantRoom = document.getElementById('occupantRoom');
let scheduleList = document.getElementById("schedule-list");

function createTime(list,result){
    let div = document.createElement("div")
          
    let idOccupant = document.createElement("input");
    idOccupant.type ="hidden";
    idOccupant.value = result.id;

    let new_time_start = document.createElement("input");
    new_time_start.type = "time";
    new_time_start.value = result.time_start;
    new_time_start.readOnly = true;

    let new_time_end = document.createElement("input");
    new_time_end.type = "time";
    new_time_end.value = result.time_end;
    new_time_end.readOnly = true;

    let new_occupant = document.createElement("input");
    new_occupant.type = 'text';
    new_occupant.value = result.occupant;
  
    if(result.occupant == null){
      new_occupant.value = "Nenhum Ocupante"
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
    edit_button.id = `edit-button-${result.id}`;
    edit_button.textContent = "Editar Horário";
    edit_button.value = result.id;
    
    edit_button.onclick  = () => edit(edit_button);

    // Guarda a URL como atributo data
    const baseUrl = window.location.origin; // ex: http://localhost:8000
    edit_button.dataset.action = `${baseUrl}/OccupancyUpdate/${result.id}`;

    // edit_button.dataset.action = `OccupancyUpdate/${result.id}`;

    let delete_button = document.createElement("button");
    delete_button.id = `delete-button-${result.id}`;
    delete_button.textContent = "Deletar Horário";
    delete_button.value = result.id;

    form.appendChild(delete_button);

    delete_button.onclick = (event)=>{
      event.preventDefault();
      removeTime(event.target,dataFormatada);
    }

    list.appendChild(div);
    div.appendChild(idOccupant);
    div.appendChild(new_time_start);
    div.appendChild(new_time_end);
    div.appendChild(new_occupant);

    div.appendChild(edit_button);
    div.appendChild(form);
}

function removeTime(button,dataFormatada){
  fetch(`/OccupancyDelete/${button.value}/`,{
    method:"POST",
    headers:{
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body:JSON.stringify({
      day: dataFormatada
    })
  })
  .then(response=>response.json())
  .then(results => {
        let list = document.getElementById("list");
        scheduleList.removeChild(list);
        let new_div = document.createElement("div")
        list = scheduleList.appendChild(new_div);
        list.id="list";
        
        results.forEach(result=>{

          // CRIAÇÃO DOS INPUTS E BOTÕES DE OCUPÂNCIA
          createTime(list,result);

        })
    })
}

flatpickr("#calendar", {
    inline: true,
    mode: "single", // Faz o calendário sempre visível
    enableTime: false, // Se quiser selecionar horário também
    dateFormat: "Y-m-d",     // formato da data
    locale: "pt" ,
    onChange: function(selectedDates, dateStr, instance) {
      console.log("Datas selecionadas:", selectedDates);
      
      // Pega a última data clicada (como objeto Date)
      let ultimaData = selectedDates[selectedDates.length - 1];
  
      // Se quiser formatar como string:
      dataFormatada = ultimaData.toISOString().split("T")[0];
      fetch(`/OccupancyCreate/${idRoom}/`,{
        method:"POST",
        headers:{
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body:JSON.stringify({
          day : dataFormatada
        })
      })
      .then(response => response.json())
      .then(results => {
          let list = document.getElementById("list");
          scheduleList.removeChild(list);
          
          let new_div = document.createElement("div")
          list = scheduleList.appendChild(new_div);
          list.id="list";
          
          results.forEach(result=>{
            // CRIAÇÃO DOS INPUTS E BOTÕES DE OCUPÂNCIA
            createTime(list,result);
          })
      })
      
      }  
  });

function addTime(){
    console.log(occupantRoom.value);
    fetch(`/OccupancyCreate/${idRoom}/`,{
      method:"POST",
      headers:{
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body:JSON.stringify({
        day : dataFormatada,
        time_start : time_start.value,
        time_end : time_end.value,
        occupant : occupantRoom.value
      })
    })
    .then(response => response.json())
    .then(results => {
        let list = document.getElementById("list");
        scheduleList.removeChild(list);
        let new_div = document.createElement("div")
        list = scheduleList.appendChild(new_div);
        list.id="list";
        
        results.forEach(result=>{

          // CRIAÇÃO DOS INPUTS E BOTÕES DE OCUPÂNCIA
          createTime(list,result);

        })
    })
}

function edit(edit_button){
  const actionUrl = edit_button.dataset.action;

  window.location.href = actionUrl;
}