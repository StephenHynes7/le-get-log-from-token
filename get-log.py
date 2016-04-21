import requests
import json
import ConfigParser
import time
import datetime

config = ConfigParser.ConfigParser()
params = {}


def load_config():
    config.read('config.ini')


def get_params():

    params['account-key'] = config.get('Auth', 'account-key')
    params['log-token'] = config.get('Auth', 'log-token')


def get_log():
    url = 'https://api.logentries.com/%s/hosts/' % params.get('account-key')
    req = requests.get(url)
    if req.status_code == 200:
        response_data = req.json()
        for host in response_data['list']:
            key = host['key']
            new_url = 'https://api.logentries.com/%s/hosts/%s/' % (params.get('account-key'), key)
            new_req = requests.get(new_url)
            if new_req.status_code == 200:
                host_data = new_req.json()
                for log in host_data['list']:
                    try:
                        print 'Searching in log %s in host %s' % (log['name'], host['name'])
                        if log['token'] == str(params.get('log-token')):
                            print '!!!!!!!'
                            print 'Found matching log %s in host %s' % (log['name'], host['name'])
                            print '!!!!!!!'
                            return
                    except KeyError:
                        pass
        print 'No log could be found for token %s' % params.get('log-token')

def start():
    load_config()
    get_params()
    get_log()


if __name__ == '__main__':
    start()