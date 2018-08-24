import os
from flask import Flask,Blueprint, render_template
import json
from . import db

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)
	db.init_app(app)


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

	# a simple page that says hello
	@app.route('/')
	def Homepage():
		with open('./flaskr/static/basic.json' , 'r') as f:
			data = json.load(f)

		return render_template('index.html', tabs=data['tabs'], emotions=data['emotions'], star_color=data['star_color'], task_list=data['task_list'],hormones=data['hormones'])

	return app


if __name__ == "__main__":
	app = create_app()
	app.config['TEMPLATES_AUTO_RELOAD']=True
	app.run(debug=True,use_reloader=True)	