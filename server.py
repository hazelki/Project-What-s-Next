from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from model import connect_to_db, db, User, Event, Saved_Event, Category, Event_Category
from flask import Flask, jsonify
from flask_mail import Mail, Message
from sqlalchemy import extract
from twilio.rest import TwilioRestClient



app = Flask(__name__)
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'awesomeeventsf@gmail.com',
    MAIL_PASSWORD = 'izmirsf12'
    )
mail = Mail(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "alskdjf7246ryoiq4h5pn2u93m4"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

# @app.route('/login', methods=['GET'])
# def login_form():
#     """Show login form."""

#     return render_template("dashboard.html") 
#     # render_template when GET method


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id


    flash("Logged in")
    
    return redirect("/dashboard")
   

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    # firstname = request.form["firstname"]
    # lastname = request.form["lastname"]
    # phone = request.form["phone"]


    # Syntax how to save it in to db
    new_user = User(email=email, password=password) 

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added" % email)
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    """After logined in user come to dashboad page and see saved events."""
    # print session
    user = User.query.get(session["user_id"])

    saved_events = Saved_Event.query.filter_by(user_id=user.user_id).all()

    eventsarray = []
    for saved_event in saved_events:
       event = saved_event.event
       eventsarray.append(event)

    # [saved_event1, saved_event2]
    # [saved_event1.event, saved_event2.event]
    organized_events = Event.query.filter_by(organizer=user.user_id).all()
    # print organized_events
    eventslist = []
    for event in organized_events:
       eventslist.append(event)

    return render_template("dashboard.html", user=user, saved_events=eventsarray, organized_events=eventslist)

@app.route("/event_list_form")
def event_list_from():
    """Displaying form for search by location and date"""
    
    return render_template('event_list_form.html')
    #return render_template('/')
    
@app.route("/event_result")
def event_result():
    """Show list of events"""

    address = request.args.get('address')
    date = request.args.get('date')
    # import pdb; pdb.set_trace()
    date = datetime.strptime(date, "%Y-%m-%d")


    events_by_address = Event.query.filter(Event.date > date, Event.date < date + timedelta(days=1), 
        Event.address.like("%" + address + "%")).all()
      
   
    return render_template("event_result.html",
                                                #event_date=events_by_date, 
                                                events=events_by_address,
                                                address=address, date=date)
    # events = Event.query.order_by('title').all()
    # return render_template("search_result.html", events=events)
@app.route('/add', methods=['POST'])
def add_event():
    """Add events."""

    event_id = request.form.get("event_id")
    user_id = request.form.get("user_id")
    saved_event = Saved_Event.query.filter_by(user_id=user_id, event_id=event_id).first()
    

    user = User.query.get(session['user_id'])
    event = Event.query.get(event_id)


    #save event into database
    if saved_event is None:
        saved_event = Saved_Event(user_id=user.user_id, event_id=event.event_id)
        
        db.session.add(saved_event)
        db.session.commit()


    return "saved"


@app.route("/create_event_form")
def create_event_form():
    """Show form for adding an event."""

    return render_template("create_event.html")

@app.route('/create_event', methods=['POST'])
def create_event():
    """Create an event"""
    
    user = User.query.get(session["user_id"])
    title = request.form.get("title")
    address = request.form.get("address")
    date = request.form.get("date")
    time = request.form.get("time")
    new_date = datetime.utcnow()
    #date = new_date.strftime("%Y-%m-%d")
    event = Event(title=title, address=address, date=new_date, organizer=user.user_id)

    db.session.add(event)
    db.session.commit()

  
    flash("Your event created.")
    return redirect("/dashboard")
    #return render_template("dashboard.html", events=events, user=user)

@app.route('/twilio/<int:event_id>', methods=['POST'])
def twilio(event_id):

    user_phone = request.form.get('phone')

    event = Event.query.get(event_id)

    body = "title:{}, adress: {}, date: {}".format(event.title, event.address, event.date)

    account_sid = "AC7c9c9da138015da2f3a398a6712cafe7"
    auth_token = "30db1cff769ddaa88c88f18a07760ff7"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to=user_phone, from_="+16468469646",
                                     body=body)
    flash("Your message was sent successfully.")
    return redirect("/dashboard") 

@app.route('/email', methods=['POST'])
def send_mail():

    user = User.query.get(session['user_id'])

    event_id = request.form.get("event_id")
    event = Event.query.get(event_id)
     

    email_body = "title:{}, adress: {}, date: {}".format(event.title, event.address, event.date)
    #Message object from flash mail
    msg = Message("Your Event",
      sender="awesomeeventsf@gmail.com",
      recipients=[user.email])
    
    msg.body = "Your event details: " + email_body
    mail.send(msg)
    return 'Mail sent!'
    #return redirect("/dashboard")


@app.route('/marker_result')
def event_info():
    """search result about events."""

    # print request.args
    event_ids = request.args.get("id").split(',')

    events = Event.query.filter(Event.event_id.in_(event_ids)).all()
    
    eventslist = []
    for event in events :
       eventslist.append({
            "event_id": event.event_id,
            "title": event.title,
            "date": event.date,
            "address": event.address,
            "picture": event.picture,
            "lat": event.lat,
            "longi":event.longi
        })
    
    return jsonify(events=eventslist)

    
@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out")
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
