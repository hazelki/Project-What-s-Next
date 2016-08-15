from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime, timedelta
from model import connect_to_db, db, User, Event, Saved_Event, Category, Event_Category

from sqlalchemy import extract

app = Flask(__name__)

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


@app.route('/login')
def login_process():
    """Process login."""

    # Get form variables
    email = request.args["email"]
    password = request.args["password"]

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
    #return render_template("dashboard.html", user=user)

    

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    phone = request.form["phone"]


    # Syntax how to save it in to db
    new_user = User(email=email, password=password, firstname=firstname,
    lastname=lastname, phone=phone) 

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % firstname)
    # return render_template("dashboard.html", user=new_user)
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    """After logined in user come to dashboad page and see saved events."""
    user = User.query.get(session["user_id"])
    events = Event.query.get(event_id)

    saved_events = Saved_Event.query.filter_by(user_id=user.user_id).all()

    # Saved Events Table
    # User Id, Event Id
    #       1,    5
    #       1,    6

    return render_template("dashboard.html", user=user, saved_events=saved_events)

@app.route("/event_list_form")
def event_list_from():
    """Displaying form for search by location and date"""
    
    return render_template('event_list_form.html')
    #return render_template('/')
    
@app.route("/event_result")
def event_result():
    """Show list of events"""
# to do : get date and location from search and then query db
    picture = request.args.get('picture')
    title = request.args.get('title')
    address = request.args.get('address')
    date = request.args.get('date')
    date = datetime.strptime(date, "%Y-%m-%d")

    picture = Event.query.filter_by(picture=picture).all()
    title = Event.query.filter_by(title=title).all()
    events_by_address = Event.query.filter(Event.date > date, Event.date < date + timedelta(days=1), 
        Event.address.like("%" + address + "%")).all()
    
    
    #events_by_date = Event.query.filter(Event.date > date, Event.date < date + timedelta(days=1)).all()

    return render_template("event_result.html", title=title,
                                                picture=picture,
                                                #event_date=events_by_date, 
                                                event_address=events_by_address)
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

    # if already added
    if saved_event:
        flash("Already in your dashboard")

    #save event into database
    if not saved_event:
        saved_event = Saved_Event(user_id=user.user_id, event_id=event.event_id)
        db.session.add(saved_event)
        db.session.commit()

    
    flash("Event %s added.")
    return "event saved"

    
    # return saved_event
    # return render_template("event_result.html", saved_event=saved_event)
    #return redirect("/event_result/%s" % event_id)


# @app.route("/create_event_form")
# def create_event_form():
#     """Show form for adding an event."""

#     return render_template("create_event.html")

# @app.route('/create_event', methods=['POST'])
# def create_event():
#     """Create an event"""

# #***********category = request.form.get

#     title = request.form.get("title")
#     address = request.form.get("address")
#     date = request.form.get("date")
#     time = request.form.get("time")

#     db.session.add()
#     db.session.commit()

#     return render_template("event_created.html", 
#                             title=title, 
#                             address=address,
#                             date=date,
#                             time=time)


# @app.route('/logout')
# def logout():
#     """Log out."""

#     del session["user_id"]
#     flash("Logged Out.")
#     return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host='0.0.0.0')
