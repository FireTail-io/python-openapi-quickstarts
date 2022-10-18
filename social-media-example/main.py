#!/usr/bin/env python3
import json
from random import randint
from randomuser import RandomUser
import firetail
import datetime
import logging

from firetail import NoContent
from firetail.auditor import cloud_logger

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

def get_profile(user,id):
    return {
        "friend_id": id,
        "first_name": user.get_first_name(),
        "last_name": user.get_last_name(),
        "username": user.get_username(),
        "dob": datetime.datetime.strptime(user.get_dob(),'%Y-%m-%dT%H:%M:%S.%fZ').date().strftime("%Y-%m-%d"),
        "state": user.get_state(),
        "postcode": user.get_postcode()
        }

FRIENDS = {}
user = RandomUser.generate_users(15,{'nat': 'ca'})
for i in range(15):
    FRIENDS[str(i)] = get_profile(user[i],i)


STORYS = {
    "1": {
        "story_id": 1,
        "username": "andy",
        "story_content": "My first story!!"
    },
    "2": {
        "story_id": 2,
        "username": "andy",
        "story_content": "Beautiful weather today"
    },
    "3": {
        "story_id": 3,
        "username": "andy",
        "story_content": "I can't wait to go to the beach"
    },
    "4": {
        "story_id": 4,
        "username": "sarah",
        "story_content": "math is so hard :("
    },
    "5": {
        "story_id": 5,
        "username": "sarah",
        "story_content": "Why wait when you can do it now?"
    },
    "6": {
        "story_id": 6,
        "username": "lucy",
        "story_content": "Vacation time!"
    },

}


def health():
    return {'status': 'UP'}

def get_friends(limit):
    return {"friends": [friend for friend in FRIENDS.values() ][:limit]}



def get_friend(friend_id):
    friend = FRIENDS.get(friend_id)
    return friend or (json.dumps({'message': "Not found"}), 404)

def put_friend(friend_id):
    friend = request.json
    exists = friend_id in FRIENDS
    friend['friend_id'] = friend_id
    if exists:
        print("Found friend ", friend_id)
        try:
            FRIENDS[friend_id].update(friend)
        except:
            print("An exception occured while trying to update friend")
    else:
        friend['created'] = datetime.datetime.utcnow()
        try:
            FRIENDS[friend_id] = friend
        except:
            print("An exception occured while trying to add a new friend")
    return NoContent, (200 if exists else 201)

def delete_friend(friend_id):
    if friend_id in FRIENDS:
        print("Found friend ", friend_id)
        try:
            del FRIENDS[friend_id]
        except:
            print("Exception occured during deletion of friend")
        return NoContent, 204
    else:
        return NoContent, 404

def get_story(story_id):
    story = STORYS.get(story_id)
    return story or (json.dumps({'message': "Not found"}), 404)

def post_story(story_id):
    story = request.json
    exists = story_id in STORYS
    story['story_id'] = story_id
    if exists:
        print("Found story ", story_id)
        try:
            STORYS[story_id].update(story)
        except:
            print("An exception occured while trying to update story")
    else:
        story['created'] = datetime.datetime.utcnow()
        try:
            STORYS[story_id] = story
        except:
            print("An exception occured while trying to add a new story")
    return NoContent, (200 if exists else 201)

def delete_story(story_id):
    if story_id in STORYS:
        print("Found story ", story_id)
        try:
            del STORYS[story_id]
        except:
            print("Exception occured during deletion of story")
        return NoContent, 204
    else:
        return NoContent, 404

def get_timeline(limit):
    return {"STORYS": [story for story in STORYS.values() ][:limit]}

logging.basicConfig(level=logging.INFO)
app = firetail.App(__name__)

app.add_api('social-media-example.yaml')



if __name__ == '__main__':
    app.debug = True
    app.run(port=8080, threaded=True)
