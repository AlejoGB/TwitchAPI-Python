from twitchapi import TwitchAPI, Games
#from flask import Flask
import json
import firebase_admin
from firebase_admin import credentials, firestore, db
import logging
from datetime import datetime
import time
import sys

def get_top_100():
    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Games(
        client_data = client_data,
        verbose=False,
        log=True,
        logger='INFO'
        )
    tkn = req.get_tkn()
    resp = req.top(tkn.json(), q='first=100')
    return resp.json()

def main_loop():
    ref = db.reference('Top 100 Games')
    mins = 10
    while True: 
        #el nombre con el q se guardan podria ser un str datetime
        resp = get_top_100()
        now = datetime.now()
        data = {
            'datetime': str(now)
        }
        now_ref = ref.child(now.strftime("%Y%m%d%H%M%S"))
        for i in range(99):
            rank = resp['data'][i]
            rank_dict ={
                i: {
                    'id': rank['id'],
                    'name': rank['name']
                }
            }
            data.update(rank_dict)

        now_ref.push(data)
        time.sleep(60*mins)




if __name__ == '__main__':
    try:
        #var de init para evitar leer lo que ya esta escrito en db
        init=True
        cred = credentials.Certificate("twitch-analytics-key.json")
        app = firebase_admin.initialize_app(cred, {
                'databaseURL' : 'https://twitch-analytics-289203.firebaseio.com/'
                })
        
        main_loop()

    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)