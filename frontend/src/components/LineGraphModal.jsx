import React from "react";
import Chart from "chart.js";


export const LineGraphModal = (props) => {
    React.useEffect(() => {
      var config = {
        type: "line",
        data: {
          labels: [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
          ],
          datasets: [
            {
              label: new Date().getFullYear(),
              backgroundColor: "#3182ce",
              borderColor: "#3182ce",
              data: [65, 78, 66, 44, 56, 67, 75],
              fill: false,
            },
          ],
        },
        options: {
          maintainAspectRatio: false,
          aspectRatio: 1,
          responsive: true,
          title: {
            display: false,
            text: "Progress",
            fontColor: "white",
          },
          legend: {
            display: false,
          },
          tooltips: {
            mode: "index",
            intersect: false,
          },
          hover: {
            mode: "nearest",
            intersect: true,
          },
          scales: {
            xAxes: [
              {
                ticks: {
                  fontColor: "rgba(255,255,255,.7)",
                },
                display: true,
                scaleLabel: {
                  display: false,
                  labelString: "Month",
                  fontColor: "white",
                },
                gridLines: {
                  display: false,
                  borderDash: [2],
                  borderDashOffset: [2],
                  color: "rgba(33, 37, 41, 0.3)",
                  zeroLineColor: "rgba(0, 0, 0, 0)",
                  zeroLineBorderDash: [2],
                  zeroLineBorderDashOffset: [2],
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  fontColor: "rgba(255,255,255,.7)",
                },
                display: true,
                scaleLabel: {
                  display: true,
                  labelString: "Accuracy",
                  fontColor: "white",
                },
                gridLines: {
                  borderDash: [3],
                  borderDashOffset: [3],
                  drawBorder: false,
                  color: "rgba(255, 255, 255, 0.15)",
                  zeroLineColor: "rgba(33, 37, 41, 0)",
                  zeroLineBorderDash: [2],
                  zeroLineBorderDashOffset: [2],
                },
              },
            ],
          },
        },
      };
      var ctx = document.getElementById("line-chart-modal").getContext("2d");
      window.myLine = new Chart(ctx, config);
    }, []);
    return (
      <>
        <div className="relative flex flex-col min-w-full break-words w-full bg-blueGray-700">
          <div className="rounded-t mb-0 px-4 py-3 bg-transparent">
            <div className="flex flex-wrap items-center">
              <div className="relative w-full max-w-full flex-grow flex-1">
              </div>
            </div>
          </div>
          <div className="p-4 flex-auto">
            {/* Chart */}
            <div className="relative h-350-px">
              <canvas id="line-chart-modal"></canvas>
            </div>
          </div>
        </div>
      </>
    );
  }