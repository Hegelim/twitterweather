/* globals Chart:false, feather:false */
function startTimer(duration, display) {
  let timer = duration, minutes, seconds;
  setInterval(function () {
    minutes = parseInt(timer / 60, 10);
    seconds = parseInt(timer % 60, 10);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    display.textContent = minutes + ":" + seconds;

    if (--timer < 0) {
      timer = duration;
    }
  }, 1000);
}

document.getElementById("twitter_update").addEventListener("click", function () {
  let progress = document.createElement("div");
  progress.className = "progress";
  progress.style.height = "20px";
  progress.innerHTML = `
    <div class="progress-bar" role="progressbar" 
    id="twitter_update_progressbar"
    aria-valuemin="0"
    aria-valuemax="100"></div>
  `;
  document.getElementById("twitter_progress").appendChild(progress);

  let i = document.getElementById("twitter_select").value;
  var display = document.getElementById('twitter_progress');
  startTimer(i, display);
})

function generate_prediction(elmnt, clr) {
  $.ajax({
    type: "POST",
    url: "test.py",
    data: {param: text}
  }).done(function() {
    console.log("What?")
  });
  elmnt.style.color = clr;
}


(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()
