from flask import Flask
from flask import render_template
from flask import json
from flask import request
import random
import sys
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

users = []


@app.route("/")
def index():
	return render_template("index.html"), 200

#generate for the first time
@app.route("/generate", methods = ["POST"])
def generate():
	this_user = {} # init user
	send_data = {} # data to be sent
	post_obj = request.json	
	rc = dimension(post_obj)

	send_data["x"] = rc["x"]
	send_data["y"] = rc["y"]
	print(post_obj["spd"])
	if(post_obj["spd"]=="1"):
		send_data["speed"] = 20
	elif(post_obj["spd"]=="2"):
		send_data["speed"] = 15
	else:
		send_data["speed"] = 15

	this_user["name"] = post_obj["name"] # sets the user's name
	this_user["speed"] = send_data["speed"] # sets the user's speed
	this_user["size"] = 0
	users.append(this_user) # append it to the list of users


	return json.dumps(send_data), 200

# sends the x and y coordinates to the client
@app.route("/regenerate", methods = ["POST"])
def regenerate():
	send_data = {}
	post_obj = request.json	
	rc = dimension(post_obj)

	send_data["x"] = rc["x"]
	send_data["y"] = rc["y"]
	
	if(post_obj["spd"]=="1"):
		send_data["speed"] = 20
	elif(post_obj["spd"]=="2"):
		send_data["speed"] = 15
	else:
		send_data["speed"] = 15
	
	return json.dumps(send_data), 200

# sends the size of the snake to the server
@app.route("/size", methods = ["POST"])
def size():
	temp = {}
	obj_obj = request.json
	for i in range(len(users)):
		if obj_obj["name"] == users[i]["name"]:
			temp = users[i]

	users[users.index(temp)]["size"] += 1

	send_data = {}
	send_data["size"] = users[users.index(temp)]["size"]

	return json.dumps(send_data), 200

# used when game is over, displays scoreboard
@app.route("/over")
def api_filter():

	query_parameters = request.args
	player_name = query_parameters.get('name')
	player_score = query_parameters.get('score')

	print(player_name)
	print(player_score)

	query2 = "select player_name, score from user_score order by score desc"
	conn = get_db_connection()
	
	conn.execute("INSERT INTO user_score (player_name, score) VALUES (?, ?)",
				(player_name, player_score)
				)

	posts = conn.execute(query2).fetchall()
	conn.commit()
	conn.close()
	
	return render_template('example.html', user_score=posts), 200

#api_endpoint to refresh the scoreboard
@app.route("/refresh")
def refresh_all():
	query = "Delete from user_score"
	conn = get_db_connection()
	conn.execute(query)

	query2 = "Select player_name, score from user_score"
	posts = conn.execute(query2).fetchall()
	conn.commit()
	conn.close()
	return render_template('example.html', user_score=posts), 200

#api_endpoint to update user point (accounts to cheating, hence discouraged)
@app.route("/update_score", methods=['GET'])
def update_score():
	query_parameters = request.args

	name = query_parameters.get('name')
	score = query_parameters.get('score')

	if not (name or score):
		return page_not_found(404)

	upd_query = "update user_score set score ="+score+" where player_name='"+name+"';"

	query = "SELECT player_name, score FROM user_score order by score desc"

	conn = get_db_connection()
	conn.execute(upd_query)
	posts = conn.execute(query).fetchall()
	conn.commit()
	conn.close()

	return render_template('example.html', user_score=posts), 200

#api_endpoint to delete player record by name
@app.route("/delete_player", methods=['GET'])
def delete_player():
	query_parameters = request.args

	name = query_parameters.get('name')

	if not (name):
		return page_not_found(404)

	del_query = "delete from user_score where player_name = '"+name+"';"

	query = "SELECT player_name, score FROM user_score order by score desc"

	conn = get_db_connection()
	conn.execute(del_query)
	posts = conn.execute(query).fetchall()
	conn.commit()
	conn.close()

	return render_template('example.html', user_score=posts), 200


'''
	Function: dimensions
	 Purpose: generates a random x and y coordinate within a limit to send it the client 		 
		  in: obj
'''

def dimension(obj):
	rc = {}
	width_min = int(obj["width_min"])
	width_max = int(obj["width_max"])
	height_min = int(obj["height_min"])
	height_max = int(obj["height_max"])

	x = random_number(width_min, width_max)
	y = random_number(height_min, height_max)

	rc["x"] = x
	rc["y"] = y

	return rc

'''
	Function: random_number
	 Purpose: generates a random number between a particular range		 
		  in: min, max
'''

def random_number(min, max):
	return random.randint(min, max)


if __name__ == "__main__":
	app.run(host = "localhost", port = 2430, debug = True)