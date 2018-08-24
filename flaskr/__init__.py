import os
from flask import Flask,Blueprint, render_template, request, make_response,session
import json
from . import db
from . import login

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

	db.init_app(app)

	# Login Page
	app.register_blueprint(login.bp)

	# a simple page that says hello
	@app.route('/' , methods=["GET" , "POST"])
	def homepage():
		with open('./flaskr/static/basic.json' , 'r') as f:
			data = json.load(f)

		try:
			user_id = session['user_id']
		except:
			user_id = False
		# print(db.query_db("SELECT * FROM user"))
		return render_template('index.html', tabs=data['tabs'], emotions=data['emotions'], star_color=data['star_color'], task_list=data['task_list'],hormones=data['hormones'], in_session = user_id)


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