let dataFormatada;
const room = document.getElementById("container")
const idRoom = room.dataset.idroom;
console.log(idRoom)
const csrfToken = document.querySelector('[name=csrf-token]').content;
console.log(csrfToken)
const time_start = document.getElementById("time_start");
const time_end = document.getElementById("time_end");

const occupant = document.querySelector('select[name="occupants"]');
console.log(occupant.value)

let scheduleList = document.getElementById("schedule-list")

// const selectOption = occupant.selectOption[0]

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
      console.log("Última data clicada:", dataFormatada);
      fetch(`/OccupancyCreate/${idRoom}/`,{
        method:"POST",
        headers:{
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body:JSON.stringify({
          day : dataFormatada
          // occupant : occupant.value
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
            let div = document.createElement("div")
            
            let idOccupant = document.createElement("input");
            idOccupant.type ="hidden";
            idOccupant.value = result.id;
  
            let new_time_start = document.createElement("input");
            new_time_start.type = "time";
            new_time_start.value = result.time_start;
  
            let new_time_end = document.createElement("input");
            new_time_end.type = "time";
            new_time_end.value = result.time_end;
  
            list.appendChild(div)
            div.appendChild(idOccupant);
            div.appendChild(new_time_start);
            div.appendChild(new_time_end);
  
          })
      })
      
      }  
  });

function addTime(){
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
        // occupant : occupant.value
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
          let div = document.createElement("div")
          
          let idOccupant = document.createElement("input");
          idOccupant.type ="hidden";
          idOccupant.value = result.id;

          let new_time_start = document.createElement("input");
          new_time_start.type = "time";
          new_time_start.value = result.time_start;

          let new_time_end = document.createElement("input");
          new_time_end.type = "time";
          new_time_end.value = result.time_end;

          list.appendChild(div)
          div.appendChild(idOccupant);
          div.appendChild(new_time_start);
          div.appendChild(new_time_end);

        })
    })
}