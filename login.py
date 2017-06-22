import configparser, os, requests, io, re, pprint
config = configparser.ConfigParser()
config.read('configs.ini')

s = requests.Session()
# print(config.get('dmm', 'user'))
# print(config.get('dmm', 'pass'))
baselogin = requests.get('https://www.dmm.com/my/-/login/=/path=Sg9VTQFXDFcXFl5bWlcKGExKUVdUXgFNEU0KSVMVR28MBQ0BUwJZBwxK')
token = re.search('"token": "([a-f0-9]{32})"', baselogin.text)
dmmt = re.search('"DMM_TOKEN", "([a-f0-9]{32})"', baselogin.text)
# print(dmmt.group(1))
data = {'token' : token.group(1)}

r = requests.Request("POST", "https://www.dmm.com/my/-/login/ajax-get-token/", data=data)
pretokens = s.prepare_request(r)
pretokens.headers["DMM_TOKEN"] = dmmt.group(1)
pretokens.headers["X-Requested-With"] = "XMLHttpRequest"
tokens = s.send(pretokens)
# {"token":"99fdc59426d71af002bf013c341ac378","login_id":"dc641a3f04d76d021f0716308e6d95f0","password":"18d7081099715c55e93bed1fb257cd2b"}
f = open('./dump.txt', 'wb')
f.write(baselogin.text.encode('utf-8'));
f.close()
print(tokens.text)
