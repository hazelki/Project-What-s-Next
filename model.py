"""Models and database functions for Ratings project."""
import heapq
import time
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

    


class Event(db.Model):
    """Event"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(1000))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(1000))
    event_category = db.Column(db.String(100))
    picture = db.Column(db.String(1000))
    organizer = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event event_id=%s title=%s>" % (self.event_id, self.title)


class Saved_Event(db.Model):
    """Saved events by organizer"""

    __tablename__ = "saved_events"

    saved_events_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("saved_events", order_by=user_id))

    # Define relationship to event
    event = db.relationship("Event",
                            backref=db.backref("saved_events", order_by=event_id))


class Category(db.Model):
    """Categories"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    
class Event_Category(db.Model):
    """Categories"""

    __tablename__ = "eventcat"

    event_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)  
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), nullable=False)
    # Define relationship to category
    user = db.relationship("Category",
                           backref=db.backref("eventcat", order_by=category_id))

    # Define relationship to event
    event = db.relationship("Event",
                            backref=db.backref("eventcat", order_by=event_id)) 

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""
    print "connect_to_db"
    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///events'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
