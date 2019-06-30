var my_colours = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]

function draw_graph(json) {
	var data = [];
	var low = 100;
	for(var i = 0; i < json.length; ++i) {
		data.push({x: new Date(json[i].timestamp),
		           y: json[i].temp});
		if (json[i].temp < low) {
			low = json[i].temp;
		}
	}
	var min = Math.floor(2*(low - 0.25))/2;
	var context = $('#chart').get(0).getContext("2d");
	var chart = new Chart(context, {
		type: 'line',
		data: {
			datasets: [{
				label: 'Kitchen',
				data: data,
				borderColor: [my_colours[1]],
				backgroundColor: [my_colours[0]],
				pointRadius: 1,
				cubicInterpolationMode: 'monotone'
			}]
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
			}
		}
	});
}

function init() {
	var zone = $('#zoneselect').val();
	var timescale = $('#timescale').val();
	fetch("/temps/" + zone + "/" + timescale)
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			draw_graph(json);
		});
}


$(document).ready(function() {
	$("#zoneselect").change(init);
	$("#timescale").change(init);
	init();
});
