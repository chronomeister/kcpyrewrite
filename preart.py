# this is used to get art before it goes live.
# OBJ:
#   check for new art on blank names
#   check for seasonal art
#   seasonal vs. new?
#   upload imgur?

import requests, pprint, time, sqlite3, psycopg2

shipfile = ("sutsfoetiofu",)

# if blank no new art, head on NULLs and keep 404/discard 200
if (not shipfile[0]):
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
								WHERE api_name IS NULL
								""")
			for record in filecur:
				status = s.head("http://%s/kcs/resources/swf/ships/%s.swf" % ('203.104.248.135',record[0]))
				if (status.ok):
					shipfile.append(record[0])
s = requests.Session()
ship = s.get("http://203.104.209.71/kcs/resources/swf/ships/" + shipfile + ".swf")
while(true):
	if (ship.status_code == 200):
		break
	else:
		time.sleep(5)
