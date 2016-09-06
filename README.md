## Synopsis

What's Next is a web application that allows users to search for and create events. Users search events by location and date, and the app aggregates local listings. Each search result includes details of the event such as title, date and the address. Each result includes a map marker showing the event location. What's Next helps users avoid the endless search since they can save search results to their dashboard to view later. Users can send themselves SMS and email reminders about upcoming saved events so they always know what they have planned. What's Next helps users save time by providing a one stop place to find, save and be reminded of all of the events they want to go to.  Event App also provides a Eventbrite API for its' events in JSON. 
It uses Google Maps API to show event locatons. PostgreSQL and SQLAlchemy store saved search results to be viewable by the user anytime. SMS text reminders for any saved event can be sent from the application via the Twilio API.  

![homepage](/homepage.jpg?raw=true "Homepage")

Create Event:
![createeventpage](/static/create_event.jpg?raw=true "Create Event Page")

Search Events:
![searcheventpage](/static/search_event.jpg?raw=true "Search for the Events")

Event Result Page: 
![Eventresultpage](/static/event_result.jpg?raw=true"Event Result Page")

Dashboard: 
![Dashboard](/static/dashboard.jpg?raw=true"Saved events")



## Installation
Event App requires a requirements.txt file installation. Event app runs through the server.py file on http://localhost:5000/


## API Reference

Event App runs on a local database. Events provided by Eventbrite Api (https://www.eventbrite.com/developer/v3/endpoints/events/). Text messages are provided by Twilio(https://www.twilio.com/docs/). Created event data is saved locally. Search result map provided by Google map Api (https://developers.google.com/maps/)

Data was saved locally to prevent API call expenses, and improve runtime. 

## Tests

Tests for Event App are located in tests.py . Event App offers 57% test coverage through unittests. Testing covers assertions on all pages on Event App, and ensures that when a user search for events a city information is displayed in search result page. 

Testing does not cover querying the database, hence the low percentage.

![coverageHTML](/static/coverage.jpg?raw=true "Testing Coverage")

## Tech Stack
Python, Javascript, JQuery, Jinja, Flask, SQL, SQLAlchemy, ajax, HTML, CSS, Coverage 


