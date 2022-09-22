from bottle import route, run, request
import requests
import json


@route("/webhook",method=["POST"])
def acceptingPost():
    token=""
    body = request.json
    if body["object"]:
        if  body["entry"] and body["entry"][0]["changes"] and body["entry"][0]["changes"][0] and body["entry"][0]["changes"][0]["value"]["messages"] and body["entry"][0]["changes"][0]["value"]["messages"][0]:
            phone_number_id =body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            senderNumber= body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            msg_body1 = body["entry"][0]["changes"][0]["value"]["messages"][0]
            msg_body=frozenset(msg_body1)
            messagesBody=json.loads({body:msg_body})
            url = f"https://graph.facebook.com/v14.0/{phone_number_id}/messages?access_token={token}"
            headers = {'Content-Type': 'application/json'}
            data={"messaging_product": "whatsapp","to": senderNumber,"text": messagesBody}
            response = requests.request("POST", url, headers=headers, data=data)
            return 200
        else:
            return 403
            
@route("/webhook",method=["GET"])
def getrequestsuest():
    verify_token = ""
    mode = request.query["hub.mode"]
    token = request.query["hub.verify_token"]
    challenge = request.query["hub.challenge"]
    if mode and token:
        if mode == "subscribe" and token == verify_token:
            return 200
        else:
            return 403

run(host="localhost",port=5050,debug=True)