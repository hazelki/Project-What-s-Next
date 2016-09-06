import unittest
from unittest import TestCase
from model import connect_to_db, db, User, Event, Saved_Event, Category, Event_Category, connect_to_db, db
from server import app
# import server


class FlaskTestsBasic(TestCase):
    """Flask tests."""


    def setUp(self):
        """Stuff to do before every test."""
        # db.init_app(app)
        print "setUp"
        connect_to_db(app)

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False



        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""
        print "tear"
        db.session.close()
        

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("<legend>Register</legend>", result.data)

   

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

        # Connect to database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""
        
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "ilkekirtis@gmail.com",
                                        "password": "ilke"},
                                  follow_redirects=True)
        self.assertIn("Logged in", result.data)

    def test_register(self):
        """Test register page."""

        result = self.client.post("/register",
                                   data={"user_id": 1,
                                        "email": "hazname@gmail.com",
                                        "password": "123"},
                                  follow_redirects=True)
        self.assertNotIn("User added", result.data)
                                    

    def test_fail_login(self):

        result = self.client.post("/login",
                                  data={"email": "ilkekirtis@gmail.com",
                                        "password": "beach"},
                                  follow_redirects=True)
        self.assertIn("Incorrect password", result.data)

    def test_logout(self):

        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("Logged Out", result.data)


    def test_create_event(self):
        """Test create event page."""

        result = self.client.post('/create_event',
                                 data={'title': 'blue',
                                 'address': 'San Francisco',
                                 'date': '2016-09-10T12:00:00Z'})
        self.assertNotIn('Event Time:', result.data)

    def test_dashboard(self):
        """Test saved event page."""

        result = self.client.get("/dashboard")
        self.assertIn("Saved Events", result.data)


    def test_search_page(self):
        """Test search page."""

        result = self.client.get("/event_list_form")
        self.assertIn("<h2>Search for Events</h2>", result.data)

  


if __name__ == "__main__":
    import unittest

    unittest.main()