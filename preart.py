# this is used to get art before it goes live.
# OBJ:
#   pivot on known / unknown new art
#   seasonal vs. new?
#   upload imgur?

import requests, pprint, time

shipfile = "sutsfoetiofu"

s = requests.Session()
ship = s.get("http://203.104.209.71/kcs/resources/swf/ships/" + shipfile + ".swf")
if (ship.status_code == 200):
	
else:
	time.sleep(5)
