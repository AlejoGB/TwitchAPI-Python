import requests
import logging
from datetime import datetime



class TwitchAPI:
    def __init__(self, client, verbose=False, log=False, *args, **kwargs):

        self.verbose = verbose
        self.log = 'logging.'+log # INFO DEBUG WARNING ERROR CRITICAL


        logging.basicConfig(format='%(lineno)d - %(asctime)s -%(filename)s - %(levelname)s : %(message)s'
                                            level=logging.INFO,
                                            filename = 'loggerTemplate.log', 
                                            #, filemode = 'w'
                                            #,  
                                            )


    def print(self, string=''):
        if self.verbose:
            print(string)
            

    def make_request(self, url):
        self.print('Requesting from > {}'.format(url))
        logging.info('Requesting from > {}'.format(url))
        try:
            response = requests.get(
                url=url,
                timeout=self.timeout,
                headers={'Client-ID': self.client_id})
        except Exceptions as e:
            return False

        self.last_status = response.status_code
        self.print('Response with status code > {}'.format(self.last_status))
        logging.info('Response with status code > {}'.format(self.last_status))
        try:
            json_data = response.json()
        except json.decoder.JSONDecodeError as e:
            self.print('Error parsing JSON: {}'.format(e))
            logging.error('Error parsing JSON: {}'.format(e))
            return False

        return json_data

    class games:
        def __init__(self, *args, **kwargs):

        def top():
            response = self.make_request()
