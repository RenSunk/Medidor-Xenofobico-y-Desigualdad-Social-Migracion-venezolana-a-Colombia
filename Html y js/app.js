let lista = document.getElementById("lista");
let tipodegrafica = "";
var chart;

document.getElementById("submit").addEventListener("submit", (event) => {
  event.preventDefault();
  let fechaI = document.getElementById("fechaI").value;
  let fechaF = document.getElementById("fechaF").value;
  let ubicacion = document.getElementById("ubicacion").value;

  if (fechaI !== "" && fechaF !== "") {
    lista.innerHTML = `
    <div class="spinner">
    <div class="lds-spinner">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
    </div>`;
    fetch(`http://127.0.0.1:5000/filter/${fechaI}/${fechaF}/${ubicacion}`)
      .then((response) => response.json())
      .then((data) => {
        lista.innerHTML = "";
        for (let i = 1; i <= Object.keys(data).length; i++) {
          lista.innerHTML += `
          <div class="contenido">   
              <img src=${data[i].imagen} />
              <div>
                  <p> ID : ${data[i].id} </p>
                  <p> Nombre : ${data[i].nombre} </p>
                  <p> Tweet : ${data[i].texto} </p>
                  <p class="${ data[i].xenofobico == "Es xenofobico" ? "rojo" : "verde"}" > ${data[i].xenofobico} </p>
                  <br/>
              </div>
          </div>
          `;
        }
        if (JSON.stringify(data) === "{}") {
          alert("vacio!!!");
        }
      });
  } else {
    alert("falta rellenar campos!!!");
  }
});

fetch("http://127.0.0.1:5000/data/10")
  .then((response) => response.json())
  .then((data) => {
    for (let i = 1; i <= Object.keys(data).length; i++) {
      lista.innerHTML += `
        <div class="contenido">   
            <img src=${data[i].imagen} />
            <div>
                <p> ID : ${data[i].id} </p>
                <p> Nombre : ${data[i].nombre} </p>
                <p> Tweet : ${data[i].texto} </p>
               
                <p class="${ data[i].xenofobico == "Es xenofobico" ? "rojo" : "verde"}" > ${data[i].xenofobico} </p>
                <br/>
            </div>
        </div>
        `;
    }
  });

// Get the modal
var modal1 = document.getElementById("myModal1");

// Get the button that opens the modal
var btn1 = document.getElementById("myBtn1");

// Get the <span> element that closes the modal
var span1 = document.getElementsByClassName("close1")[0];

// Get the modal
var modal4 = document.getElementById("myModal4");

// Get the <span> element that closes the modal
var span4 = document.getElementsByClassName("close4")[0];

// Get the modal
var modal3 = document.getElementById("myModal2");

// Get the <span> element that closes the modal
var span3 = document.getElementsByClassName("close2")[0];

// When the user clicks the button, open the modal
btn1.onclick = function () {
  modal1.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span1.onclick = function () {
  modal1.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal1) {
    modal1.style.display = "none";
  }
};

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");
var btn2 = document.getElementById("myBtn2");
var btn3 = document.getElementById("myBtn3");
var graficar = document.getElementById("graficar");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
  tipodegrafica = "Xenofobico";
  modal1.style.display = "none";
  modal.style.display = "block";
};

btn2.onclick = function () {
  tipodegrafica = "Polaridad";
  modal1.style.display = "none";
  modal.style.display = "block";
};

btn3.onclick = function () {
  tipodegrafica = "WordCloud";
  modal1.style.display = "none";
  modal4.style.display = "block";
};

span4.onclick = function () {
  modal4.style.display = "none";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

function grafi(data) {
  let keys = [""];
  Object.keys(data).forEach((element) => {
    keys.push(element);
  });
  let values = [""];
  Object.values(data).forEach((element) => {
    values.push(element);
  });
  modal3.style.display = "block";
  let canvas = document.getElementById("canvas");
  let input = document.getElementsByName("grafica");
  let graf = "";

  input.forEach((element) => {
    if (element.checked) {
      graf = element.value;
    }
  });
  if (graf === "Bar chart") {
    if (chart) {
      chart.destroy();
    }
    chart = new Chart(canvas, {
      type: "bar",
      data: {
        labels: keys,
        datasets: [
          {
            label: "Grafica de Barras",
            data: values,
            backgroundColor: [
              "rgba(181, 215, 239, 0.2)",
              "rgba(0 , 239, 163, 0.2)",
              "rgba(255, 131, 30, 0.2)",
              "rgba(30, 34, 255, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(30, 255, 101, 0.2)",
            ],
            borderColor: [
              "rgba(181, 215, 239, 1)",
              "rgba(0 , 239, 163, 1)",
              "rgba(255, 131, 30, 1)",
              "rgba(30, 34, 255, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(30, 255, 101, 1)",
            ],
            borderWidth: 2,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  } else if (graf === "Pie chart") {
    if (chart) {
      chart.destroy();
    }
    chart = new Chart(canvas, {
      type: "pie",
      data: {
        labels: Object.keys(data),
        datasets: [
          {
            label: "Grafica de Torta",
            data: Object.values(data),
            backgroundColor: [
              "rgba(0 , 239, 163, 0.2)",
              "rgba(255, 131, 30, 0.2)",
              "rgba(30, 34, 255, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(30, 255, 101, 0.2)",
            ],
            borderColor: [
              "rgba(0 , 239, 163, 1)",
              "rgba(255, 131, 30, 1)",
              "rgba(30, 34, 255, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(30, 255, 101, 1)",
            ],
            borderWidth: 2,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  } else if (graf === "Line chart") {
    if (chart) {
      chart.destroy();
    }
    chart = new Chart(canvas, {
      type: "line",
      data: {
        labels: Object.keys(data),
        datasets: [
          {
            label: "Grafica de linea",
            data: Object.values(data),
            fill: false,
            borderColor: "rgb(224, 153, 0)",
            backgroundColor: "rgb(224, 153, 0)",
            tension: 0.01,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
}

graficar.onclick = function () {
  let fechaIM = document.getElementById("fechaIM").value;
  let fechaFM = document.getElementById("fechaFM").value;
  if (tipodegrafica == "Xenofobico") {
    fetch(`http://127.0.0.1:5000/db/${fechaIM}/${fechaFM}/si`)
      .then((data) => data.json())
      .then((data) => {
        grafi(data);
      });
  } else if (tipodegrafica == "Polaridad") {
    fetch(`http://127.0.0.1:5000/db/${fechaIM}/${fechaFM}/no`)
      .then((data) => data.json())
      .then((data) => {
        grafi(data);
      });
  } else {
  }
};
let Btnwordcloud = document.getElementById("Btnwordcloud");

Btnwordcloud.onclick = function () {
  if (chart) {
    chart.destroy();
  }
  let fechaIW = document.getElementById("fechaIW").value;
  let fechaFW = document.getElementById("fechaFW").value;
  let Btnwordcloud = document.getElementById("Btnwordcloud").value;
  let ubicacionW = document.getElementById("ubicacionW").value;

  modal3.style.display = "block";
  let canvas = document.getElementById("canvas");

  list = [];

  fetch(`http://127.0.0.1:5000/frecuencia/${fechaIW}/${fechaFW}/${ubicacionW}`)
    .then((data) => data.json())
    .then((datos) => {
      console.log(datos[ubicacionW])
      for (var i in datos[ubicacionW]) {
        list.push([datos[ubicacionW][i]["word"], datos[ubicacionW][i]["freq"]*10]);
      }
      
      WordCloud.minFontSize = "1000px"
      WordCloud(document.getElementById('canvas'), { 
        clearCanvas: true,
        list: list,
        drawOutOfBound : false,
        shrinkToFit : true,
        backgroundColor: "#B5D7EF"
      } );
    })
}

// When the user clicks on <span> (x), close the modal
span3.onclick = function () {
  modal3.style.display = "none";
};
