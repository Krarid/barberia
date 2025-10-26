/********* Bar char *********/
const xArray = ["Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
const yArray = [49, 44, 24, 32, 23, 64];

const data = [{
  x: xArray,
  y: yArray,
  type: "bar",
  orientation:"v",
  marker: {color:"rgba(0,0,255)"}
}];

const layout = {title:"Cortes mensuales"};

Plotly.newPlot("myPlot", data, layout);

/********* Donut char *********/
const donutData = [{labels:xArray, values:yArray, hole:.4, type:"pie"}];

Plotly.newPlot("myPlot2", donutData, layout);