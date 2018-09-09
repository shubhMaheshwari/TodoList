#!/bin/bash
cd ~/TodoList

export FLASK_APP=flaskr
export FLASK_ENV=development

# if [ -f "venv" ]
# then 
# 	echo "Virtual env already present"
# else
# 	virtualenv venv
# fi

# cd venv/bin/
# source activate	
# cd ../../

if [ $# -ne 1 ] 
	then
	flask run
	exit 0	
fi


if [ $1 = "prod" ];
	then
	export FLASK_ENV=production
	python3 run.py

elif [ $1 = "clean" ];
	then
	new_dir="old_instance$(date "+%F-%T")"
	mv instance $new_dir
	rm -rf flaskr/__pycache__
elif [ $1 = "help" ];
	then 
	echo "Usage ./run.sh <argument>" 1>&2 
	echo "Arguments: start(default), help, clean, init"
	exit 0
elif [ $1 = "start" ];
	then
	flask run
elif [ $1 = "init" ];
	then
	flask init-db
elif [ $1 = "kill" ];
	then
	todo_process_id=$(lsof -i:5000 -t)
	kill -9 $todo_process_id 
else
	echo "Usage ./run.sh <argument>" 1>&2 
	echo "Arguments: start(default), help, clean, init_db"
	exit 0
fi
