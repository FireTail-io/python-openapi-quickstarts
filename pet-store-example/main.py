#!/usr/bin/env python3
import json
from random import randint
from randomuser import RandomUser
import pointsecio
import datetime
import logging

from pointsecio import NoContent
from pointsecio.auditor import request_auditor

# our memory-only pet storage
from pointsecio.exceptions import OAuthProblem
from requests import get

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


PETS = {
    "1": {
        "pet_id": 1,
        "pet_type": "fish",
        "pet_name": "goldfish",
        "pet_status": "available"
    },
    "2": {
        "pet_id": 2,
        "pet_type": "fish",
        "pet_name": "clownfish",
        "pet_status": "pending"
    },
    "3": {
        "pet_id": 3,
        "pet_type": "fish",
        "pet_name": "catfish",
        "pet_status": "available"
    },
    "4": {
        "pet_id": 4,
        "pet_type": "fish",
        "pet_name": "rasboras",
        "pet_status": "pending"
    },
    "5": {
        "pet_id": 5,
        "pet_type": "fish",
        "pet_name": "bettafish",
        "pet_status": "sold"
    },
    "6": {
        "pet_id": 6,
        "pet_type": "cat",
        "pet_name": "persian",
        "pet_status": "sold"
    },
    "7": {
        "pet_id": 7,
        "pet_type": "cat",
        "pet_name": "siberian",
        "pet_status": "available"
    },
    "8": {
        "pet_id": 8,
        "pet_type": "cat",
        "pet_name": "bobtail",
        "pet_status": "sold"
    },
    "9": {
        "pet_id": 9,
        "pet_type": "dog",
        "pet_name": "bulldog",
        "pet_status": "available"
    },
    "10": {
        "pet_id": 10,
        "pet_type": "dog",
        "pet_name": "poodle",
        "pet_status": "pending"
    },
    "11": {
        "pet_id": 11,
        "pet_type": "dog",
        "pet_name": "boxer",
        "pet_status": "sold"
    },
    "12": {
        "pet_id": 12,
        "pet_type": "dog",
        "pet_name": "pug",
        "pet_status": "available"
    },
    "13": {
        "pet_id": 13,
        "pet_type": "turtle",
        "pet_name": "spotted",
        "pet_status": "available"
    },
    "14": {
        "pet_id": 14,
        "pet_type": "parrot",
        "pet_name": "green",
        "pet_status": "available"
    },
    "15": {
        "pet_id": 15,
        "pet_type": "hamster",
        "pet_name": "hamster",
        "pet_status": "available"
    },
}




def health():
    return {'status': 'UP'}

def get_pets(limit, pet_type=None):
    print("pet_type: ", pet_type)
    return {"pets": [pet for pet in PETS.values() if not pet_type or pet['pet_type'] == pet_type][:limit]}

def get_available_pets():
    return {"pets": [pet for pet in PETS.values() if pet['pet_status'] == "available"]}

def get_pet(pet_id):
    pet = PETS.get(pet_id)
    return pet or ("Not found", 404)

def put_pet(pet_id, pet):
    exists = pet_id in PETS
    pet['pet_id'] = pet_id
    if exists:
        print("Found pet ", pet_id)
        try:
            PETS[pet_id].update(pet)
        except:
            print("An exception occured while trying to update pet")
    else:
        print("Did not Find pet..will try to create a new pet ", pet_id)
        pet['created'] = datetime.datetime.utcnow()
        try:
            PETS[pet_id] = pet
        except:
            print("An exception occured while trying to create a pet")
    return NoContent, (200 if exists else 201)

def delete_pet(pet_id):
    if pet_id in PETS:
        print("Found pet ", pet_id)
        try:
            del PETS[pet_id]
        except:
            print("Exception occured during deletion of pet")
        return NoContent, 204
    else:
        return NoContent, 404

def get_pet_availability(pet_id):
    exists = pet_id in PETS
    if exists:
        counter = randint(1,10)
        if(counter > 5):
            message = "pet " + pet_id + " is available"
        else:
            message = "pet " + pet_id + " is not available"
        return json.dumps({"message": message}), 200
    else:
        return NoContent, 404

def put_reservation():
    counter = randint(1,10)
    if(counter > 5):
        message = "reservation has been made successfully"
    else:
        message = "reservation failed"
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
app = pointsecio.App(__name__)

app.add_api('pet-store-example.yaml')



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, threaded=True)
