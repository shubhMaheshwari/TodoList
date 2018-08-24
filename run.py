import os
from flaskr import create_app



if __name__ == "__main__":
	app = create_app()
	app.config['TEMPLATES_AUTO_RELOAD']=True
	app.run(debug=True,use_reloader=True)	