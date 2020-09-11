from twitchapi import TwitchAPI, Games
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
        verbose=False,
        log=True,
        logger='INFO'
    )
    tkn = req.get_tkn()    
    resp = req.top(tkn.json(), q='first=100') #first , after , before (pagination)
    #print(resp.json())
    assert resp.status_code == HTTP_STATUS_SUCCESS


#'{"access_token":"13fpj33mq3gqi0oeb3oxyk7lqq66q5","expires_in":5197431,"token_type":"bearer"}\n'


