import requests
import logging
from datetime import datetime
import json

# TODO: los metodos y clases tienen que devolver resp , resp.status_code

class TwitchAPI:
    def __init__(self, client_data, verbose=False, log=False, timeout=10,*args, **kwargs):
        self.client_data = client_data
        self.timeout = timeout
        self.urls = self.get_urls('urls.json')# endpoints
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
            

    def make_request(self, url, tkn):
        self.print('Requesting from > {}'.format(url))
        logging.info('Requesting from > {}'.format(url))
        try:
            response = requests.get(
                url=url,
                timeout=self.timeout,
                headers={
                    'Client-ID': self.client_data['client_id'],
                    'Authorization': tkn['token_type'].capitalize() + " " + tkn['access_token']
                })
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
        print(response.content)
        print(response.status_code)
        return response


class Games(TwitchAPI):
#    def __init__(self, client_data, verbose=False, log=False, timeout=10,*args, **kwargs):
#        super().__init__(client_data, verbose=False, log=False, timeout=10,*args, **kwargs)

    def top(self, tkn):
        response = self.make_request(self.urls['games']['top'], tkn)
        if response:
            return response
        else:
            logging.error('No data retrieved from TOP GAMES request')
            raise Exception('No data retrieved from request')
        pass
            
            
