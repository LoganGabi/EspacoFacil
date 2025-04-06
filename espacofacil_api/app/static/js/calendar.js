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
// const selectOption = occupant.selectOption[0]

flatpickr("#calendar", {
    inline: true,
    mode: "multiple", // Faz o calendário sempre visível
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
        occupant : occupant.value
      })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    })
}