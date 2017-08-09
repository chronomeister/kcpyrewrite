import configparser, os, requests, io, re, pprint, json, time, math
config = configparser.ConfigParser()
config.read('configs.ini')

servers = ("203.104.209.71", "203.104.209.87", "125.6.184.16", "125.6.187.205", "125.6.187.229", "125.6.187.253", "125.6.188.25", "203.104.248.135", "125.6.189.7", "125.6.189.39", "125.6.189.71", "125.6.189.103", "125.6.189.135", "125.6.189.167", "125.6.189.215", "125.6.189.247", "203.104.209.23", "203.104.209.39", "203.104.209.55", "203.104.209.102")

s = requests.Session()
# print(config.get('dmm', 'user'))
# print(config.get('dmm', 'pass'))
baselogin = s.get('https://www.dmm.com/my/-/login/=/path=Sg9VTQFXDFcXFl5bWlcKGExKUVdUXgFNEU0KSVMVR28MBQ0BUwJZBwxK')
token = re.search('"token": "([a-f0-9]{32})"', baselogin.text)
dmmt = re.search('"DMM_TOKEN", "([a-f0-9]{32})"', baselogin.text)
s.cookies.set("ckcy","1", domain="www.dmm.com", path="/netgame/", expires="1549682583000")
data = {'token' : token.group(1)}

r = requests.Request("POST", "https://www.dmm.com/my/-/login/ajax-get-token/", data=data)
pretokens = s.prepare_request(r)
pretokens.headers["DMM_TOKEN"] = dmmt.group(1)
pretokens.headers["X-Requested-With"] = "XMLHttpRequest"
tokens = s.send(pretokens)
agt = tokens.json()
data = { \
	"token" : agt["token"], \
	"login_id" : config.get('dmm', 'user'), \
	"save_login_id" : 0, \
	"password" : config.get('dmm', 'pass'), \
	"save_password" : 0, \
	"use_auto_login" : 0, \
	agt["login_id"] : config.get('dmm', 'user'), \
	agt["password"] : config.get('dmm', 'pass'), \
	"path" : 'Sg9VTQFXDFcXFl5bWlcKGExKUVdUXgFNEU0KSVMVR28MBQ0BUwJZBwxK', \
	"prompt" : None, \
	"client_id" : None, \
	"display" : None \
}
auth = s.post("https://www.dmm.com/my/-/login/auth/", data=data)
# go to app page now.
basegame = s.get('http://www.dmm.com/netgame/social/-/gadgets/=/app_id=854854/')
viewerre = re.search('VIEWER_ID[^\d"]+([\d"]+)',basegame.text)
viewid = viewerre.group(1)
stre = re.search('(?: )+ST(?: )+(?:: )"([^\r\n"]+)',basegame.text)
st = stre.group(1)
dmmtime = math.floor(time.time() * 1000)

data = { \
	"refresh" : 3600, \
	"url" : "http://203.104.209.7/kcsapi/api_world/get_id/" + viewid + "/1/" + str(dmmtime), \
	"httpMethod" : "GET", \
	"headers" : "", \
	"postData" : "", \
	"authz" : "", \
	"st" : "", \
	"contentType" : "JSON", \
	"numEntries" : "3", \
	"getSummaries" : "false", \
	"signOwner" : "true", \
	"signViewer" : "true", \
	"gadget" : "http://203.104.209.7/gadget.xml", \
	"container" : "dmm", \
	"bypassSpecCache" : "", \
	"getFullHeaders" : "false" \
}
worldfound = False
worldre = None
while (not worldfound):
	worldform = s.get('http://osapi.dmm.com/gadgets/makeRequest?' + '&'.join(['%s=%s' % (key, value) for (key, value) in data.items()]))
	worldre = re.search(r'\\"api_world_id\\":(\d+)',worldform.text)
	if (worldre):
		worldfound = True
	else:
		time.sleep(10)
servip = servers[int(worldre.group(1))-1]

data = { \
	"url" : "http://" + servip + "/kcsapi/api_auth_member/dmmlogin/" + viewid + "/1/" + str(dmmtime), \
	"httpMethod" : "GET", \
	"headers" : "", \
	"postData" : "", \
	"authz" : "signed", \
	"st" : st, \
	"contentType" : "JSON", \
	"numEntries" : "3", \
	"getSummaries" : "false", \
	"signOwner" : "true", \
	"signViewer" : "true", \
	"gadget" : "http://203.104.209.7/gadget.xml", \
	"container" : "dmm", \
	"bypassSpecCache" : "", \
	"oauthState" : "", \
	"getFullHeaders" : "false" \
}
main = s.post("http://osapi.dmm.com/gadgets/makeRequest", data=data)
tokenre = re.search(r'\\"api_token\\":\\"([0-9a-f]+)',main.text)
token = tokenre.group(1)
f = open('./api.txt', 'w')
f.write("http://" + servip + "/kcs/mainD2.swf?api_token=" + token);
f.close()
print("Your api link is : http://" + servip + "/kcs/mainD2.swf?api_token=" + token)
