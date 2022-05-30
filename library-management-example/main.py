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

from pointsecio import request

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


BOOKS = {
    "1": {
        "book_id": 1,
        "book_title": "Avengers",
        "book_type": "action",
        "book_author": "andy",
        "book_availability": True
    },
    "2": {
        "book_id": 2,
        "book_title": "B-Team",
        "book_type": "action",
        "book_author": "andy",
        "book_availability": True
    },
    "3": {
        "book_id": 3,
        "book_title": "Cats",
        "book_type": "action",
        "book_author": "chris",
        "book_availability": True
    },
    "4": {
        "book_id": 4,
        "book_title": "Dentistry",
        "book_type": "action",
        "book_author": "sandy",
        "book_availability": True
    },
    "5": {
        "book_id": 5,
        "book_title": "Explosive",
        "book_type": "action",
        "book_author": "bob",
        "book_availability": True
    },
   "6": {
        "book_id": 6,
        "book_title": "Fight club",
        "book_type": "comedy",
        "book_author": "bob",
        "book_availability": True
    },
    "7": {
        "book_id": 7,
        "book_title": "Going home",
        "book_type": "comedy",
        "book_author": "rachel",
        "book_availability": True
    },
    "8": {
        "book_id": 8,
        "book_title": "Holiday",
        "book_type": "comedy",
        "book_author": "patrick",
        "book_availability": True
    },
    "9": {
        "book_id": 9,
        "book_title": "In paradise",
        "book_type": "comedy",
        "book_author": "patrick",
        "book_availability": True
    },
    "10": {
        "book_id": 10,
        "book_title": "Joker",
        "book_type": "comedy",
        "book_author": "shelly",
        "book_availability": True
    },
    "11": {
        "book_id": 11,
        "book_title": "Karnival",
        "book_type": "romance",
        "book_author": "ash",
        "book_availability": True
    },
    "12": {
        "book_id": 12,
        "book_title": "Love",
        "book_type": "romance",
        "book_author": "andy",
        "book_availability": True
    },
    "13": {
        "book_id": 13,
        "book_title": "Moonlight sky",
        "book_type": "romance",
        "book_author": "patrick",
        "book_availability": True
    },
    "14": {
        "book_id": 14,
        "book_title": "Titanic",
        "book_type": "romance",
        "book_author": "john",
        "book_availability": True
    },
    "15": {
        "book_id": 15,
        "book_title": "Mayfeather days",
        "book_type": "romance",
        "book_author": "andy",
        "book_availability": True
    },
    "16": {
        "book_id": 16,
        "book_title": "Goosebumps",
        "book_type": "horror",
        "book_author": "bob",
        "book_availability": True
    },
    "17": {
        "book_id": 17,
        "book_title": "The Hill",
        "book_type": "horror",
        "book_author": "andy",
        "book_availability": True
    },
}




def health():
    return {'status': 'UP'}

def get_books(limit, book_type=None):
    print("book_type: ", book_type)
    return {"books": [book for book in BOOKS.values() if not book_type or book['book_type'] == book_type][:limit]}

def get_books_by_author(limit, book_author=None):
    print("book author: ", book_author)
    return {"books": [book for book in BOOKS.values() if not book_author or book['book_author'] == book_author][:limit]}
def get_book(book_id):
    book = BOOKS.get(book_id)
    return book or ("Not found", 404)

def put_book(book_id):
    book = request.json
    exists = book_id in BOOKS
    book['book_id'] = book_id
    if exists:
        print("Found book ", book_id)
        try:
            BOOKS[book_id].update(book)
        except:
            print("An exception occured while trying to update book")
    else:
        print("Did not Find book, will try to create a new book ", book_id)
        book['created'] = datetime.datetime.utcnow()
        try:
            BOOKS[book_id] = book
        except:
            print("An exception occured while trying to create a book")
    return NoContent, (200 if exists else 201)

def delete_book(book_id):
    if book_id in BOOKS:
        print("Found book ", book_id)
        try:
            del BOOKS[book_id]
        except:
            print("Exception occured during deletion of book")
        return NoContent, 204
    else:
        return NoContent, 404

def get_book_availability(book_id):
    exists = book_id in BOOKS
    if exists:
        counter = randint(1,10)
        if(counter > 5):
            message = "book " + book_id + " is available"
        else:
            message = "book " + book_id + " is not available"
        return json.dumps({"message": message}), 200
    else:
        return NoContent, 404

def put_reservation():
    counter = randint(1,10)
    if(counter > 5):
        message = "Reservation has been made successfully"
    else:
        message = "Reservation failed"
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

app.add_api('library-management-example.yaml')



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, threaded=True)
