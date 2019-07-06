var my_colours = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"];

var myChart = null;

function draw_graph(json) {
	var datasets = [];
	var low = 100;
	for(var i = 0; i < json.length; ++i) {
		var data = [];
		for(var j = 0; j < json[i].data.length; ++j) {
			data.push({x: new Date(json[i].data[j].timestamp),
								y: json[i].data[j].temp});
			if (json[i].data[j].temp < low) {
				low = json[i].data[j].temp;
			}
		};
		dataset = {
				borderColor: [my_colours[2*i+1]],
				backgroundColor: [my_colours[2*i]],
				pointRadius: 3,
				cubicInterpolationMode: 'monotone',
				label: json[i].label,
				data: data
		};
		datasets.push(dataset);
	}
	var min = Math.floor(2*(low - 0.25))/2;
	if (myChart != undefined) {
		myChart.destroy();
	}
	var context = $('#chart').get(0).getContext("2d");
	myChart = new Chart(context, {
		type: 'line',
		data: {
			datasets: datasets
		},
		options: {
			scales: {
				xAxes: [{
					type: 'time'
				}],
				yAxes: [{
					ticks: {
						suggestedMin: min
					}
				}]
			},
			tooltips: {
				callbacks: {
					label: function(tooltipItem, data){
						return "Temp: " + Number(tooltipItem.yLabel).toFixed(2)
									+ "°C";
					}
				}
			}
		}
	});
}

function init() {
	var timescale = $('#timescale').val();
	fetch("/temps/" + timescale)
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			draw_graph(json);
		});
}


$(document).ready(function() {
	$("#timescale").change(init);
	init();
});
