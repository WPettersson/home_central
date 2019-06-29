var my_colours = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"]

function make_graph(json) {
	var data = [];
	for(var i = 0; i < json.length; ++i) {
		data.push({x: new Date(json[i].timestamp),
		           y: json[i].temp});
	}
	console.log(data);
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
				}]
			}
		}
	});
}

function init() {
	// Read data
	fetch("/temps/1/24")
		.then(function(response) {
			return response.json();
		})
		.then(function(json) {
			make_graph(json);
		});
}

$(document).ready(init);
