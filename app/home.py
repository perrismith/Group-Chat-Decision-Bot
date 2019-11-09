from flask import Flask, request
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response

    #name = request.values.get('From')
    #message = '{} has messaged {} {} times.' \
     #   .format(name, request.values.get('To'))

    # Put it in a TwiML response
    message = request.values.get("Body")
    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run()
