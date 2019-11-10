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

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

    body = str(request.values.get("Body"))
    resp = MessagingResponse()

    print("Body \n {}".format(body))

    if (re.match(r'Add me', body)):
        NUMBERS.append(str(request.values.get("From")))
        print(NUMBERS)
        resp.message("Ok! You are added!")
        return str(resp)
    
    if (re.match(r'Deactivate', body)):
        NUMBERS.remove(str(request.values.get("From")))
        print(NUMBERS)
        resp.message("Ok! I'll remove you!")
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


    resp.message("Ok! You are added!")
    return str(resp)


if __name__ == "__main__":
    app.run()
