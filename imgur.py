import configparser, os, requests, io, re, pprint

config = configparser.ConfigParser()
config.read('configs.ini')
sec = config.get('imgur', 'secret')
iid = config.get('imgur', 'id')


req = requests.request('POST', 'https://api.imgur.com/oauth2/tokens', headers={'Authorization':'Client-ID '+ iid}, \
   params={'client_id' : iid, 'response_type' : 'token'})

pprint.pprint(req.url)
pprint.pprint(req.content)
