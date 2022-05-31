#!/usr/bin/env python3
import json
from random import randint
from typing import List
import pointsecio
import datetime
import logging

from pointsecio import NoContent
from pointsecio.auditor import request_auditor

# our memory-only pet storage
from pointsecio.exceptions import OAuthProblem
from requests import get

from flask import jsonify
from werkzeug.exceptions import HTTPException

from pointsecio import request
debug = True  # global variable setting the debug config




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




class User:
    def __init__(self,id,username,firstName,lastName,email,password,phone,userStatus):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phone = phone
        self.userStatus = userStatus


ORDERS = {
    "1": {
        "id": 1,
        "petId": 1,
        "quantity": 100,
        "shipDate": datetime.datetime.strftime(datetime.datetime.now(),"%x"),
        "status":"placed",
        "complete": True
    },
    "2": {
        "id": 2,
        "petId": 1,
        "quantity": 50,
        "shipDate": datetime.datetime.strftime(datetime.datetime.now(),"%x"),
        "status":"approved",
        "complete": True
    },
    "3": {
        "id": 3,
        "petId": 1,
        "quantity": 50,
        "shipDate": datetime.datetime.strftime(datetime.datetime.now(),"%x"),
        "status":"delivered",
        "complete": True
    }
}


PETS = {
    "1": {
        "id": 1,
        "category": {
            "id": 2,
            "name": "Cats"
            },
        "name": "Cat 1",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag1"
            },
            {
                "id": 1,
                "name": "tag2"
            }
        ],
        "status": "available"
    },
    "2": {
        "id": 2,
        "category": {
            "id": 2,
            "name": "Cats"
            },
        "name": "Cat 2",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag2"
            },
            {
                "id": 1,
                "name": "tag3"
            }
        ],
        "status": "available"
    },
    "3": {
        "id": 3,
        "category": {
            "id": 2,
            "name": "Cats"
            },
        "name": "Cat 3",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag3"
            },
            {
                "id": 1,
                "name": "tag4"
            }
        ],
        "status": "pending"
    },
    "4": {
        "id": 4,
        "category": {
            "id": 1,
            "name": "Dogs"
            },
        "name": "Dog 1",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag1"
            },
            {
                "id": 1,
                "name": "tag2"
            }
        ],
        "status": "available"
    },
    "5": {
        "id": 5,
        "category": {
            "id": 1,
            "name": "Dogs"
            },
        "name": "Dog 2",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag2"
            },
            {
                "id": 1,
                "name": "tag3"
            }
        ],
        "status": "sold"
    },
    "6": {
        "id": 6,
        "category": {
            "id": 1,
            "name": "Dogs"
            },
        "name": "Dog 3",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag3"
            },
            {
                "id": 1,
                "name": "tag4"
            }
        ],
        "status": "pending"
    },
    "7": {
        "id": 7,
        "category": {
            "id": 4,
            "name": "Lions"
            },
        "name": "Lion 1",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag1"
            },
            {
                "id": 1,
                "name": "tag2"
            }
        ],
        "status": "available"
    },
    "8": {
        "id": 8,
        "category": {
            "id": 4,
            "name": "Lions"
            },
        "name": "Lion 2",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag2"
            },
            {
                "id": 1,
                "name": "tag3"
            }
        ],
        "status": "available"
    },
    "9": {
        "id": 9,
        "category": {
            "id": 4,
            "name": "Lions"
            },
        "name": "Lion 3",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag3"
            },
            {
                "id": 1,
                "name": "tag4"
            }
        ],
        "status": "available"
    },
    "10": {
        "id": 10,
        "category": {
            "id": 3,
            "name": "Rabbits"
            },
        "name": "Rabbit 1",
        "photoUrls": ["url1","url2"],
        "tags": [
            {
                "id": 0,
                "name": "tag1"
            },
            {
                "id": 1,
                "name": "tag2"
            }
        ],
        "status": "available"
    }
}


USERS = {
    "1" : {
        "id": 1,
        "username": "user1",
        "firstName": "first name 1",
        "lastName": "last name 1",
        "email": "email1@test.com",
        "password": "123",
        "phone": "123-456-7890",
        "userStatus": 1
    },
    "2" : {
        "id": 2,
        "username": "user2",
        "firstName": "first name 2",
        "lastName": "last name 2",
        "email": "email2@test.com",
        "password": "123",
        "phone": "123-456-7890",
        "userStatus": 2
    },
    "3" : {
        "id": 3,
        "username": "user3",
        "firstName": "first name 3",
        "lastName": "last name 3",
        "email": "email3@test.com",
        "password": "123",
        "phone": "123-456-7890",
        "userStatus": 3
    },
    "4" : {
        "id": 4,
        "username": "user4",
        "firstName": "first name 4",
        "lastName": "last name 4",
        "email": "email4@test.com",
        "password": "123",
        "phone": "123-456-7890",
        "userStatus": 1
    },
    "5" : {
        "id": 5,
        "username": "user1",
        "firstName": "first name 5",
        "lastName": "last name 5",
        "email": "email5@test.com",
        "password": "123",
        "phone": "123-456-7890",
        "userStatus": 2
    },
}


def addPet():
    try:
        newPet = request.json
        id = str(newPet["id"])
        PETS[id] = newPet
        return json.dumps(PETS[id]), 200
    except:
        print("An exception occured")
        return NoContent, 400


def updatePet():
    try:
        newPet = request.json
        id = str(newPet["id"])
        exists =  id in PETS
        if exists:
            PETS[id] = newPet
        return NoContent, (200 if exists else 404)
    except:
        print("An exception occured")
        return NoContent, 400

def findPetsByStatus(status):
    pets = []
    for pet in PETS.values():
        if pet["status"] in status:
            pets.append(pet)
    return json.dumps(pets), 200

def findPetsByTags(tags):
    pets = []
    for pet in PETS.values():
        for singleTag in tags:
            for petTag in pet["tags"]:
                if singleTag in petTag["name"]:
                    pets.append(pet)
    return json.dumps(pets),200

def getPetById(petId):
    if str(petId) in PETS:
        return json.dumps(PETS[str(petId)]),200
    return NoContent, 404

def updatePetWithForm(petId, name, status):
    exists =  str(petId) in PETS
    if exists:
        PETS[str(petId)]["name"] = name
        PETS[str(petId)]["status"] = status
        print(PETS[str(petId)])
    return NoContent, (200 if exists else 404)

def deletePet(petId):
    exists =  str(petId) in PETS
    if exists:
        PETS.pop(str(petId))
    return NoContent, (200 if exists else 404)

def uploadFile(petId,additionalMetadata):
    exists =  str(petId) in PETS
    if exists:
        PETS[str(petId)]["photoUrls"].append(additionalMetadata)
    return NoContent, (200 if exists else 404)

def getInventory():
    inventory = {}
    for order in ORDERS.values():
        if order["status"] in inventory:
            inventory[order["status"]] = inventory.get(order["status"]) + order["quantity"]
        else:
            inventory[order["status"]] = order["quantity"]
    return json.dumps(inventory)

def placeOrder():
    newOrder = request.json
    id = str(newOrder["id"])
    ORDERS[id] = newOrder
    return NoContent, 200

def getOrderById(orderId):
    if str(orderId) in ORDERS:
        return json.dumps(ORDERS[str(orderId)])
    return NoContent, 404

def deleteOrder(orderId):
    exists =  str(orderId) in ORDERS
    if exists:
        ORDERS.pop(str(orderId))
    return NoContent, (200 if exists else 404)

def createUser():
    newUser = request.json
    id = str(newUser["id"])
    print("Creating user id ", id)
    USERS[id] = newUser
    return USERS[id], 200

def createUsersWithListInput():
    users = request.json
    for user in users:
        USERS[str(user["id"])] = user
    return NoContent, 200

def createUsersWithArrayInput():
    users = request.json
    for user in users:
        USERS[str(user["id"])] = user
    return NoContent, 200

def createUsersWithArrayInput():
    users = request.json
    for user in users:
        USERS[str(user["id"])] = user
    return NoContent, 200

def loginUser(username, password):
    return {"message": "<replace with return message>"}, 200

def logoutUser():
    return {"message": "<replace with return message>"}, 200

def getUserByName(username):
    for user in USERS.values():
        if user["username"] == username:
            print("Found user")
            return json.dumps(user), 200
    return NoContent, 404

def updateUser(username):
    newUser = request.json
    for user in USERS.values():
        if user["username"] == username:
            USERS[str(user["id"])] = newUser
            return json.dumps(USERS[str(newUser["id"])]), 200
        return NoContent, 404

def deleteUser(username):
    for user in USERS.values():
        if user["username"] == username:
            USERS.pop(str(user["id"]))
            return NoContent, 200
    return NoContent,  404


logging.basicConfig(level=logging.INFO)
app = pointsecio.App(__name__)

app.add_api('swagger.yaml')

@app.app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e

    res = {'code': 500,
           'errorType': 'Internal Server Error',
           'errorMessage': "Something went really wrong!"}
    if debug:
        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'

    return jsonify(res), 500

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, threaded=True)
