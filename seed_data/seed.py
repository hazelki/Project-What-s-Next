import datetime
from model import connect_to_db, db, User, Event, Saved_Event, Category, Event_Category
from server import app
import requests
import json
from flask_sqlalchemy import SQLAlchemy


def load_events():
	"Load events from data.json into database"

	data = open("seed_data/data.json").read()
	data = json.loads(data)

	event_data = {}
	for event in data.keys():
	
		event_data = data["picture"]
		event_data = data["title"]
		event_data = data["date"]
		event_data = data["address"]

	print event

#add to the session 

	db.session.add(events)

	#commit the work 
	db.session.commit()



	# print "Events"

	# for row in enumerate(open("seed_data/data.json")):
	# row = row.rstrip()

	# event_id, title, date, location, event_category, picture, organizer = row.split(",")

	# event = Event(title=title,
	# 	          date=date,
	# 	          location=location,
	# 	          event_category=event_category,
	# 	          picture=picture,
	# 	          organizer=organizer)

		          

	
