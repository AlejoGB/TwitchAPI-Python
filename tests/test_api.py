from api.twitchapi import TwitchAPI, Games, Channels
import pytest
import json

# T D D 
HTTP_STATUS_SUCCESS = 200




def test_get_tkn():
    with open('client_data.json') as f:
        client_data = json.load(f)    

    req = TwitchAPI(
        client_data = client_data,
        verbose=False,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    assert tkn.status_code == HTTP_STATUS_SUCCESS

def test_get_top_games():
    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Games(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()    
    resp = req.top(tkn.json())
    #print(resp.json())
    assert resp.status_code == HTTP_STATUS_SUCCESS

def test_get_top_games_params():
    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Games(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()    
    resp = req.top(tkn.json(), q='first=100') #first , after , before (pagination)
    assert resp.status_code == HTTP_STATUS_SUCCESS

def test_get_games():
    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Games(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    q = 493057

    resp = req.detail(tkn.json(), id=q)
    assert resp.status_code == HTTP_STATUS_SUCCESS

def test_search_channels():
    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Channels(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    name='glitchgirl'
    
    resp = req.search(tkn.json(), search=name)
    assert resp.status_code == HTTP_STATUS_SUCCESS


def test_search_channels_params():
    # TODO: LIVE_ONLY NOT WORKING
    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Channels(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    name='glitchgirl'
    
    resp = req.search(tkn.json(), search=name, live_only=True)
    assert resp.status_code == HTTP_STATUS_SUCCESS


def test_get_streams():

    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Channels(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    game_id = 493057
    resp = req.get_streams(tkn.json())
    print(resp.content)
    assert resp.status_code == HTTP_STATUS_SUCCESS


def test_get_streams_params1():

    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Channels(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    language = 'español'
    q = 'first=30'

    resp = req.get_streams(tkn.json(), language=language, q=q)
    assert resp.status_code == HTTP_STATUS_SUCCESS

def test_get_streams_params2():

    with open('client_data.json') as f:
        client_data = json.load(f)
    req = Channels(
        client_data = client_data,
        verbose=True,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()
    user_login = 'mrdonbrown'
    q = 'first=30'

    resp = req.get_streams(tkn.json(), user_login=user_login, q=q)
    assert resp.status_code == HTTP_STATUS_SUCCESS