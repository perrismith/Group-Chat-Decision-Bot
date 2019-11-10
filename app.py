import os
import re
import random
from flask import Flask, request
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']
client = Client(account_sid, auth_token)

NUMBERS = []
VALS = []

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

    body = str(request.values.get("Body"))
    resp = MessagingResponse()

    print("Body \n {}".format(body))

    if (re.match(r'Add me', body)):
        num = request.values.get("From")

        if num not in NUMBERS:
            NUMBERS.append(str(request.values.get("From")))
            resp.message("Ok! You are added!")
        else:
            resp.message("You are already added!")

        print(NUMBERS)
        return str(resp)
    
    if (re.match(r'Deactivate', body)):
        num = request.values.get("From")

        if num in NUMBERS:
            NUMBERS.remove(str(request.values.get("From")))
            resp.message("Ok! You are removed!")
        else:
            resp.message("You aren't in the chat! Respond with 'Add me' to join.")

        print(NUMBERS)
        return str(resp)

    if (re.match(r'Add: (.+)', body)):
        val = re.match(r'Add: (.+)', body)
        val = val[1]

        if val not in VALS:
            VALS.append(val)
            resp.message("Ok! I added {}!".format(val))
        else:
            resp.message("{} is already an option!".format(val))

        print(VALS)
        return str(resp)

    if (re.match(r'Make a decision!', body)):

        if (len(VALS) == 0):
            resp.message("Add an option using 'Add: option'")
            return str(resp)

        ran = random.randrange(len(VALS))
        resp = MessagingResponse()
        
        decision = "I choose ... {}!".format(VALS[ran]) 
        resp.message(decision) 

        for num in NUMBERS:
            message = client.messages.create( body=decision,
                                        from_= os.environ['TWILIO_NUMBER'],
                                        to=num
            )
        
        VALS.clear()

        return str(resp)   

    if (re.match(r'Help me decide', body)):

        body_arr = re.findall(r'\d\. ([a-zA-Z]+ *[a-zA-Z]*)', body)

        ran = random.randrange(len(body_arr))

        resp = MessagingResponse()

        if (len(body_arr) == 0):
            resp.message("Sorry try again.")
            return str(resp)

        decision = "I choose ... {}!".format(body_arr[ran])        
        
        resp.message(decision) 

        for num in NUMBERS:
            message = client.messages.create( body=decision,
                                        from_= os.environ['TWILIO_NUMBER'],
                                        to=num
            )
        
        return str(resp) 
    return str(resp)


if __name__ == "__main__":
    app.run()
