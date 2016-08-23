import datetime
from model import connect_to_db, db, User, Event, Saved_Event, Category, Event_Category
from server import app
import requests
import json
from flask_sqlalchemy import SQLAlchemy


def load_events():
	"Load events from dataeventbrite.json into database"

	print ("*")*20, "loading event bright!", ("*")*20
	data = open("seed_data/data.json").read()
	
	data = json.loads(data)
	counter= 0

	# event_data = {}
	for event in data:
	# row = row.rstrip()
	# event_id, title, date, location, event_category, picture, organizer = row.split(",")
#check if event at title is type ascii ,if it is event then "contiune"
		# if type(event["title"]) == ascii:
		# 	contiune
		print event['title']
		
		event_db = Event(title=event["title"],
		          date=event["date"],
		          address=event["address"],
		          picture=event["picture"])

		print event_db

	#add to the session 

		db.session.add(event_db) 
		counter = counter + 1
		print counter

	#commit the work 
	db.session.commit()

def load_events_eventful():
	"Load events from dataeventful.json into database"

	print ("*")*20, "loading eventful!", ("*")*20
	data = open("seed_data/data_eventful.json").read()
	
	data = json.loads(data)
	counter= 0

	# event_data = {}
	for event in data:
	
		print event['title']
		
		eventful_db = Event(title=event["title"],
		          date=event["date"],
		          address=event["address"],
		          picture=event["picture"])

		print eventful_db

	#add to the session 

		db.session.add(eventful_db) 
		counter = counter + 1
		print counter

	#commit the work 
	db.session.commit()

if __name__=="__main__":
	connect_to_db(app)
	db.drop_all()
	db.create_all()
	load_events_eventful()
	load_events()





	


		          

	
