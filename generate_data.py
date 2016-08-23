import requests
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
token = "BRNZBA2WMA3SZZOQFZLP"
api_url = "https://www.eventbriteapi.com/v3/"
cities = ["San Francisco", "Oakland", "Fremont", "Santa Rosa", "Hayward", "Richmond", "Sunnyvale",
"Concord", "Palo Alto", "Napa", "Sonoma", "San Mateo", "Santa Clara", "Solano", "Alameda", "Contra Costa",
 "Marin", "San Jose", "Berkeley"]

events = []
city_count = 0

for city in cities:
	search_url = api_url + "/events/search/"
	result = requests.get(search_url, params={"token":token, "venue.city":city})
	search_json = result.json()
	
	event_count = 0
	for event in search_json["events"]:
		venue_url = api_url + "/venues/{}/".format(event["venue_id"])
		print venue_url
		result = requests.get(venue_url, params={"token":token, "venue.city":city})
		venue_json = result.json()
		event_data = {}
		event_data["date"] = event["start"]["local"]
		event_data["lat"] = venue_json["latitude"]
		event_data["long"] = venue_json["longitude"]
		event_data["address"] = venue_json["address"]["localized_address_display"]
		event_data["title"] = event["name"]["text"]
		event_data["picture"] = event["logo"]["url"] if event["logo"] is not None else ""
		events.append(event_data)
		event_count = event_count + 1
		print "event {} of {} for {} processed".format(event_count, len(search_json["events"]), city)

pp.pprint(events)

output = open('data.json', 'w')

output.write(json.dumps(events))

output.close()

print 'number of events:', len(events)