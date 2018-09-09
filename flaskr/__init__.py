import os
from flask import Flask,Blueprint, render_template, request, make_response,session, redirect, url_for, Response, send_from_directory
import json
from . import db
from . import login
from datetime import datetime


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)
	
	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Database
	db.init_app(app)

	# Login Page
	app.register_blueprint(login.bp)

	# Sockets
	

	# a home page with all basic UI
	@app.route('/' , methods=["GET" , "POST"])
	def homepage():
		with open('./flaskr/static/basic.json' , 'r') as f:
			data = json.load(f)

		try:
			user_id = session['user_id']
			user_tasks = db.query_db("SELECT task_id,created,deadline FROM user_task WHERE user_id = ?", (user_id,)) 
			tasks_id = [int(x['task_id']) for x in user_tasks]	
			tasks_timeleft = {}			
			if len(tasks_id) == 0:
				tasks = []
			else:
				query = "select * from todo_list where id in ({seq})".format(seq=','.join(['?']*len(tasks_id)))
				tasks = db.query_db(query, tasks_id)
				# get the deadline for the tasks
				for task in user_tasks:
					print(task['created'], task['deadline'])
					tasks_timeleft[task['task_id']] = int(100*(datetime.now() - task['created']).total_seconds()*60/task['deadline'])
			user_details = db.query_db("SELECT * FROM user WHERE id = ?", (user_id,), one=True) 
			data['emotions'][0]['value'] = user_details['Love'] // 5
			data['emotions'][1]['value'] = user_details['Reward'] // 5
			data['emotions'][2]['value'] = user_details['Sleep'] // 5
			data['emotions'][3]['value'] = user_details['Energy'] // 5
			data['emotions'][4]['value'] = user_details['Stress'] // 5
			data['emotions'][5]['value'] = user_details['Money_Credit'] // 5
		except Exception as e:
			user_id = False
			tasks = []
			emotions = {}
			tasks_timeleft = {}						
			print("Error:",e)
		# print(db.query_db("SELECT * FROM user"))
		return render_template('index.html', tabs=data['tabs'], emotions=data['emotions'], star_color=data['star_color'], activity_list=tasks,time_left=tasks_timeleft,hormones=data['hormones'], in_session = user_id)


	# Accepts post request of add activity
	@app.route('/add_activity' , methods=["POST"])
	def add_activity():
		# db.query_db("INSERT INTO todo_list ()")		
		if request.method == 'POST':
			db.add_new_task(request.form, session['user_id'])
			
		return redirect(url_for('homepage'))

	@app.route('/show_activities/')
	def show_activities():
		tasks = db.query_db("SELECT title FROM todo_list")
		resp = {}
		for task in tasks:
			resp[task['title']] = None
		return Response(json.dumps(resp),  mimetype='application/json')

	@app.route('/delete_activity/<int:activity_id>' , methods=["POST"])
	def delete_user_activity(activity_id):
		# db.query_db("INSERT INTO todo_list ()")		
		if request.method == 'POST':
			db.delete_user_task(request.form, activity_id,session['user_id'])
			
		return redirect(url_for('homepage'))

	# Error handing for 404
	@app.errorhandler(404)
	def not_found(error):
		resp = make_response(render_template('error.html'), 404)
		resp.headers['X-Something'] = 'Nothing here'
		return resp

	return app


if __name__ == "__main__":
	app = create_app()
	app.config['TEMPLATES_AUTO_RELOAD']=True
	app.run(debug=True,use_reloader=True)	