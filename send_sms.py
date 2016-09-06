# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "AC7c9c9da138015da2f3a398a6712cafe7"
auth_token = "30db1cff769ddaa88c88f18a07760ff7"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+19175204059", from_="+16468469646",
                                     body="Hello there!",
                                     media_url=['https://demo.twilio.com/owl.png', 'https://demo.twilio.com/logo.png'])


 
	                                   	