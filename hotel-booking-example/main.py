#!/usr/bin/env python3
import json
from random import randint
from randomuser import RandomUser
import firetail
import datetime
import logging

from firetail import NoContent
from firetail.auditor import request_auditor

# our memory-only pet storage
from firetail.exceptions import OAuthProblem
from requests import get

from firetail import request

TOKEN_DB = {
    'asdf1234567890': {
        'uid': 100
    }
}


def apikey_auth(token, required_scopes):
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid token')

    return info


ROOMS = {
    "1": {
        "room_id": 1,
        "room_type": "single",
        "room_availability": True
    },
    "2": {
        "room_id": 2,
        "room_type": "single",
        "room_availability": True
    },
    "3": {
        "room_id": 3,
        "room_type": "single",
        "room_availability": True
    },
    "4": {
        "room_id": 4,
        "room_type": "single",
        "room_availability": False
    },
    "5": {
        "room_id": 5,
        "room_type": "single",
        "room_availability": False
    },
   "6": {
        "room_id": 6,
        "room_type": "double",
        "room_availability": False
    },
    "7": {
        "room_id": 7,
        "room_type": "double",
        "room_availability": True
    },
    "8": {
        "room_id": 8,
        "room_type": "double",
        "room_availability": False
    },
    "9": {
        "room_id": 9,
        "room_type": "double",
        "room_availability": True
    },
    "10": {
        "room_id": 10,
        "room_type": "double",
        "room_availability": True
    },
    "11": {
        "room_id": 11,
        "room_type": "triple",
        "room_availability": True
    },
    "12": {
        "room_id": 12,
        "room_type": "triple",
        "room_availability": False
    },
    "13": {
        "room_id": 13,
        "room_type": "triple",
        "room_availability": True
    },
    "14": {
        "room_id": 14,
        "room_type": "triple",
        "room_availability": False
    },
    "15": {
        "room_id": 15,
        "room_type": "triple",
        "room_availability": False
    },
    "16": {
        "room_id": 16,
        "room_type": "Penthouse",
        "room_availability": False
    },
    "17": {
        "room_id": 17,
        "room_type": "Penthouse",
        "room_availability": True
    },
}




def health():
    return {'status': 'UP'}

def get_rooms(limit, room_type=None):
    print("room_type: ", room_type)
    return {"rooms": [room for room in ROOMS.values() if not room_type or room['room_type'] == room_type][:limit]}

def get_available_rooms():
    return {"rooms": [room for room in ROOMS.values() if room['room_availability'] == True]}

def get_room(room_id):
    room = ROOMS.get(room_id)
    return room or ("Not found", 404)

def put_room(room_id):
    room = request.json
    exists = room_id in ROOMS
    room['room_id'] = room_id
    if exists:
        print("Found room ", room_id)
        try:
            ROOMS[room_id].update(room)
        except:
            print("An exception occured while trying to update room")
    else:
        print("Did not Find room..will try to create a new room ", room_id)
        room['created'] = datetime.datetime.utcnow()
        try:
            ROOMS[room_id] = room
        except:
            print("An exception occured while trying to create a room")
    return NoContent, (200 if exists else 201)

def delete_room(room_id):
    if room_id in ROOMS:
        print("Found room ", room_id)
        try:
            del ROOMS[room_id]
        except:
            print("Exception occured during deletion of room")
        return NoContent, 204
    else:
        return NoContent, 404

def get_room_availability(room_id):
    exists = str(room_id) in ROOMS
    if exists:
        counter = randint(1,10)
        if(counter > 5):
            message = "Room " + room_id + " is available"
        else:
            message = "Room " + room_id + " is not available"
        return json.dumps({"message": message}), 200
    else:
        return json.dumps({"message": "invalid room id"}), 404

def put_booking():
    counter = randint(1,10)
    if(counter > 5):
        message = "Booking has been made successfully"
    else:
        message = "Booking failed"
    return json.dumps({"message": message}), 200

def get_profile():
    user = RandomUser({'nat': 'ca'})
    return {
        "first_name": user.get_first_name(),
        "last_name": user.get_last_name(),
        "username": user.get_username(),
        "dob": datetime.datetime.strptime(user.get_dob(),'%Y-%m-%dT%H:%M:%S.%fZ').date(),
        "state": user.get_state(),
        "postcode": user.get_postcode()
        }



logging.basicConfig(level=logging.INFO)
app = firetail.App(__name__)

app.add_api('openapi-3.0.yaml')



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, threaded=True)
