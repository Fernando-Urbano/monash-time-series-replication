import React from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';

function MetricChart({ data }) {
  const models = Object.keys(data);
  let datasetsNamesSet = new Set();

  models.forEach(model => {
    Object.keys(data[model]).forEach(dataset => {
      datasetsNamesSet.add(dataset);
    });
  });
  const datasetsNames = Array.from(datasetsNamesSet);

  const chartData = {
    labels: datasetsNames,
    datasets: models.map((model, index) => {
      return {
        label: model,
        data: datasetsNames.map(datasetName => data[model][datasetName] || 0),
        borderColor: rainbow(models.length, index),
        // borderColor: getRandomColor(),
        backgroundColor: 'transparent',
        pointRadius: 5,
        pointHoverRadius: 7,
        fill: false,
      };
    }),
  };

  return <Line data={chartData} />;
}

// COLORS GENERATORS:

// RANDOM COLOR
function getRandomColor() {
  var color = "#" + ((1 << 24) * Math.random() | 0).toString(16).padStart(6, "0")
  return color;
}

// VIBRANT & "UNIQUE" COLORS
/**
 * @param numOfSteps: Total number steps to get color, means total colors
 * @param step: The step number, means the order of the color
 */
function rainbow(numOfSteps, step) {
    // This function generates vibrant, "evenly spaced" colours (i.e. no clustering). This is ideal for creating easily distinguishable vibrant markers in Google Maps and other apps.
    // Adam Cole, 2011-Sept-14
    // HSV to RBG adapted from: http://mjijackson.com/2008/02/rgb-to-hsl-and-rgb-to-hsv-color-model-conversion-algorithms-in-javascript
    var r, g, b;
    var h = step / numOfSteps;
    var i = ~~(h * 6);
    var f = h * 6 - i;
    var q = 1 - f;
    switch(i % 6){
        case 0: r = 1; g = f; b = 0; break;
        case 1: r = q; g = 1; b = 0; break;
        case 2: r = 0; g = 1; b = f; break;
        case 3: r = 0; g = q; b = 1; break;
        case 4: r = f; g = 0; b = 1; break;
        case 5: r = 1; g = 0; b = q; break;
    }
    var c = "#" + ("00" + (~ ~(r * 255)).toString(16)).slice(-2) + ("00" + (~ ~(g * 255)).toString(16)).slice(-2) + ("00" + (~ ~(b * 255)).toString(16)).slice(-2);
    return (c);
}


export default MetricChart;