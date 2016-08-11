from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Event, Saved_Event, Category, Event_Category


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

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    # return redirect("/users/%s" % user.user_id)
    return render_template("dashboard.html", user=user)



@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    new_user = User(email=email, password=password) # Syntax how to save it in to db

    db.session.add(new_user)
    db.session.commit()

    # flash("User %s added." % email)
    return render_template("dashboard.html", user=new_user)



@app.route("/event_list_form")
def event_list_from():
    """Search filter by location and date"""
    
    return render_template('event_list_form.html')
    
@app.route("/event_result")
def event_result():
    """Show list of events"""
# to do : get date and location from search and then query db
    address = request.args.get('address')

    event_address = Event.query.filter_by(address=address).all()
    print event_address
    date = request.args.get('date')

    event_available = Event.query.filter_by(date=date).all()
    print event_available

    return render_template("event_result.html", event_available=event_available, 
                                                event_address=event_address)
    # events = Event.query.order_by('title').all()
    # return render_template("search_result.html", events=events)

@app.route("/create_event_form")
def create_event_form():
    """Show form for adding an event."""

    return render_template("create_event.html")

@app.route('/create_event', methods=['POST'])
def create_event():
    """Create an event"""

#***********category = request.form.get

    title = request.form.get("title")
    address = request.form.get("address")
    date = request.form.get("date")
    time = request.form.get("time")

    db.session.add()
    db.session.commit()

    return render_template("event_created.html", 
                            title=title, 
                            address=address,
                            date=date,
                            time=time)


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
