hormones=[ 'Dopamine' ,'Seretonine' ,'Oxytocin' ,'Aderline' ,'Cortisol/Stress']
hormone_color={ 'Dopamine': 'blue' ,'Seretonine': 'yellow' ,'Oxytocin' : 'pink' ,'Aderline' : 'red','Cortisol/Stress': 'black'}

$(document).ready(function(){
    $('.modal').modal();

	$('#register_modal').modal();
	window.myLine = {}
	hormones.map( hormone => {
		var ctx = document.getElementById(hormone+"_canvas").getContext('2d');
		var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var config = {
			type: 'line',
			data: {
				label: hormone,
				labels : Array.from(Array(8).keys()),
				datasets: [{
					data: (document.getElementById(hormone + "_data").innerHTML).split(" "),
					fill: false,
					borderColor: hormone_color[hormone]
				}]
			},
			options: {
				responsive: true,
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Time'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Value'
						}
					}]
				}
			}
		};
		window.myLine[hormone] = new Chart(ctx, config);
		window.myLine[hormone].update();

	})
});


