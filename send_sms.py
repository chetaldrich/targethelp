from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect
from flask import Markup
from flask import render_template
import twilio.twiml
from twilio.rest import TwilioRestClient
from pprint import pprint

def sms():
	resp = twilio.twiml.Response()
    	msg = str(request.values['Body'])
    	l = msg.split("#")
    	a = l[0]
    	mid = " @ aisle "
    	x = l[1]
    	w = " says "
    	y = l[2]
	print l
	account_sid = "Insert Twilio account ID here"
	auth_token = "Insert Twilio auth_token here"
	client = TwilioRestClient(account_sid, auth_token)
	message = client.messages.create(body="Hey! "+x +mid +a +w +y,
	to="+16417808874", # Replace with your phone number
	from_="+16415696366") # Replace with your Twilio number
	print message.sid

if __name__ == "__main__":
    app.run(debug=True)
