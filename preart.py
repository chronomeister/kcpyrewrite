# this is used to get art before it goes live.
# OBJ:
#   check for new art on blank names
#   check for seasonal art
#   seasonal vs. new?
#   upload imgur?

import requests, pprint, time, sqlite3, psycopg2

shipfiles = {"sutsfoetiofu" : 0}

# if blank no new art, head on NULLs and keep 404/discard 200
seasonal = True
s = requests.Session()
if (not shipfile[0]):
	seasonal = false
	with psycopg2.connect(dbname=pgdb, host=pghost, user=pguser, password=pgpass) as fndb:
		with fndb.cursor() as filecur:
			filecur.execute( """SELECT api_filename
								FROM jsonb_to_recordset((
								  SELECT start2->'api_data'->'api_mst_shipgraph'
								  FROM kcjson ORDER BY apidate DESC LIMIT 1))
								a(api_filename TEXT, api_id INT)
								LEFT JOIN jsonb_to_recordset((
								  SELECT start2->'api_data'->'api_mst_ship'
								  FROM kcjson ORDER BY apidate DESC LIMIT 1))
								b(api_name TEXT, api_id INT) USING (api_id)
								WHERE api_name IS NULL AND (api_id < 800 OR api_id > 1500)
								""")
			for record in filecur:
				status = s.head("http://%s/kcs/resources/swf/ships/%s.swf".format('203.104.248.135',record[0]))
				if (not status.ok):
					shipfiles[record[0]] = s.headers['content-length']
else:
	for ship in shipfiles:
		filesize = s.head("http://203.104.209.71/kcs/resources/swf/ships/%s.swf".format(ship))
		shipfiles[ship] = s.headers['content-length']
# ship = s.get("http://203.104.209.71/kcs/resources/swf/ships/" + shipfile + ".swf")
done = False
while(not done):
	for ship in shipfiles:
		status = s.get("http://203.104.209.71/kcs/resources/swf/ships/%s.swf".format(ship), stream=True)
		done = done || (status.headers['content-length'] == shipfiles[ship]))
	if (not done ):
		time.sleep(5)
	else:
		time.sleep(2)
