import requests
import logging
from datetime import datetime
import json
from pathlib import Path
import urllib.parse


# TODO: output should be: resp , resp.status_code

URLS_PATH = str(Path(__file__).parent) + '/urls.json'



class TwitchAPI:
    def __init__(self, client_data, verbose=False, log=False, timeout=10,*args, **kwargs):
        self.client_data = client_data
        self.timeout = timeout
        self.urls = self.get_urls(URLS_PATH)# endpoints
        self.verbose = verbose
        if log:
            self.log = 'logging.'+ kwargs.get('logger','error').upper() # INFO DEBUG WARNING ERROR CRITICAL
        self.last_status = 0

        logging.basicConfig(format='%(lineno)d - %(asctime)s -%(filename)s - %(levelname)s : %(message)s',
                                            level=eval(self.log),
                                            filename='logs/api.log', 
                                            #, filemode = 'w'
                                            #,  
                                            )

    def get_urls(self, path):
        with open(path) as f:
            return json.load(f)

    
    def get_tkn(self):
        try:
            response = requests.post(self.urls['oauth_token'] ,data=self.client_data, timeout=self.timeout)
        except Exception as e:
            self.print('Request stopped by an exception: {}'.format(e))
            logging.error('Request stopped by an exception: {}'.format(e))
            return False 
        self.print('Token request returned with status code > {}'.format(response.status_code))
        logging.info('Token request returned with status code > {}'.format(response.status_code))
        self.last_status = response.status_code
        return response


    def print(self, string=''):
        if self.verbose:
            print(string)
        pass
            

    def make_request(self, url, tkn, *args, **kwargs):
        ''' kwargs = keword de parametros de query en url'''

        self.print('Requesting from > {}'.format(url))
        logging.info('Requesting from > {}'.format(url))
        if kwargs.get('param'):
            try:
                response = requests.get(
                    url=url,
                    params=kwargs.get('param'),
                    timeout=self.timeout,
                    headers={
                        'Client-ID': self.client_data['client_id'],
                        'Authorization': tkn['token_type'].capitalize() + " " + tkn['access_token']},
                        )
                
            except Exception as e:
                self.print('Request stopped by an exception: {}'.format(e))
                logging.error('Request stopped by an exception: {}'.format(e))
                return False
        else:
            try:
                response = requests.get(
                    url=url,
                    timeout=self.timeout,
                    headers={
                        'Client-ID': self.client_data['client_id'],
                        'Authorization': tkn['token_type'].capitalize() + " " + tkn['access_token']},
                        )
            except Exception as e:
                self.print('Request stopped by an exception: {}'.format(e))
                logging.error('Request stopped by an exception: {}'.format(e))
                return False

        self.last_status = response.status_code
        self.print('Response with status code > {}'.format(self.last_status))
        logging.info('Response with status code > {}'.format(self.last_status))
        # try:
        #     json_data = response.json()
        # except json.decoder.JSONDecodeError as e:
        #     self.print('Error parsing JSON: {}'.format(e))
        #     logging.error('parsing JSON: {}'.format(e))
        #     return False

        # return json_data
        return response


class Games(TwitchAPI):
#    def __init__(self, client_data, verbose=False, log=False, timeout=10,*args, **kwargs):
#        super().__init__(client_data, verbose=False, log=False, timeout=10,*args, **kwargs)

    def top(self, tkn, *args, **kwargs):
        ''' kwargs:
        q='first=100'
        after before first (pagination)
        https://dev.twitch.tv/docs/api/reference#get-top-games'''

        response = self.make_request(self.urls['games']['top'], tkn, params=kwargs.get('q'))
        if response:
            return response
        else:
            logging.error('No data retrieved from TOP GAMES request')
            raise Exception('No data retrieved from request')


    def detail(self, tkn, *args, **kwargs):
        ''' kwargs:
        id = interger (game id)
        name = string (game name)   '''
        if kwargs.get('id'):
            param = 'id='+str(kwargs.get('id'))
        if kwargs.get('name'):
            param = 'name='+kwargs.get('name')
        
        response = self.make_request(self.urls['games']['detail'], tkn, param=param)
        if response:
            return response
        else:
            logging.error('No data retrieved from TOP GAMES request')
            raise Exception('No data retrieved from request')

        
class Channels(TwitchAPI):
#    def __init__(self, client_data, verbose=False, log=False, timeout=10,*args, **kwargs):
#        super().__init__(client_data, verbose=False, log=False, timeout=10,*args, **kwargs)

    def search(self, tkn, *args, **kwargs):
        ''' kwargs:
        name ='FollowGrubby'
        live_only=True
        q='first=100'
        after first (pagination)
        https://dev.twitch.tv/docs/api/reference#search-channels'''
        # TODO: agregar que el kwarg search pueda ser mas de una palabra
        if kwargs.get('search'):
            param = 'query=' + kwargs.get('search')
            if kwargs.get('live_only'):
                param = param + '&live_only=' + str(kwargs.get('live_only'))
            if kwargs.get('q'):
                param = param + '&' + kwargs.get('q')
        response = self.make_request(self.urls['channels']['search'], tkn, param=param)
        if response:
            return response
        else:
            logging.error('No data retrieved from TOP GAMES request')
            raise Exception('No data retrieved from request')
    