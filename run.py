from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def App():

	tabs = [
		{'id': 'hormones',
		'name': 'Hormones'},
		{'id': 'tasks',
		'name': 'Tasks'},
		{'id': 'emotions',
		'name': 'Emotions'}
		]

	emotions = [{'name': 'Trust',
		'value' : 5},
		{'name': 'Confidence',
		'value' : 5},
		{'name': 'Reward',
		'value' : 5},
		{'name': 'Sleep',
		'value' : 5},
		{'name': 'Energy',
		'value' : 5},
		{'name': 'Stress',
		'value' : 5},
		{'name': 'Money',
		'value' : 5}
		]

	task_list = [{'name': 'Sleep 8 hours', 'periodic':True, 'periodic_time': '24 hours'},
		{'name': 'DIP Assignment 2', 'periodic':False, 'deadline': '12:00' },
		{'name': 'CP', 'periodic':True, 'periodic_time': '12 hours'}
		]

	star_color = ['red' , 'red', 'red', 'yellow', 'yellow', 'yellow', 'blue' , 'blue', 'green' , 'green']

	hormones=[{'name' : 'Dopamine' , "data": ' '.join([str(x) for x in range(8) ])},
		{'name' : 'Seretonine' , "data": ' '.join([str(x) for x in range(8) ])},
		{'name' : 'Oxytocin' , "data": ' '.join([str(x) for x in range(8) ])},
		{'name' : 'Aderline' , "data": ' '.join([str(x) for x in range(8) ])},
		{'name' : 'Cortisol/Stress' , "data": ' '.join([str(x) for x in range(8) ])}]
	print(hormones[0])

	return render_template('index.html', tabs=tabs, emotions=emotions, star_color=star_color, task_list=task_list,hormones=hormones)


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=True,use_reloader=True)	