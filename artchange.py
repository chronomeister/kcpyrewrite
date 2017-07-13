# this is used to get art before it goes live.
# OBJ:
#   pivot on known / unknown new art
#   seasonal vs. new?
#   upload imgur?

import requests, pprint, time, sqlite3, psycopg2, configparser

config = configparser.ConfigParser()
config.read('configs.ini')
pghost = config.get('postgres', 'host')
pguser = config.get('postgres', 'username')
pgpass = config.get('postgres', 'password')
pgdb = config.get('postgres', 'db')

ships = ( \
	"sutsfoetiofu", \
)
filelist = []
with psycopg2.connect(dbname=pgdb, host=pghost, user=pguser, password=pgpass) as fndb:
	with fndb.cursor() as filecur:
		filecur.execute("""SELECT api_filename FROM jsonb_to_recordset((SELECT start2->'api_data'->'api_mst_shipgraph' FROM kcjson ORDER BY apidate DESC LIMIT 1)) a(api_filename TEXT)""")
		for record in filecur:
			filelist.append(record[0])

con = sqlite3.connect('kcshipimage')
con.execute("""CREATE TABLE IF NOT EXISTS basefile (filename TEXT, length INT, sha1 TEXT)""")
con.execute("""CREATE TABLE IF NOT EXISTS imagefile (filename TEXT, imgnum INT, length INT, sha1 TEXT)""")
con.execute("""CREATE TEMP TABLE tmpbasefile (filename TEXT, length INT, sha1 TEXT)""")
con.execute("""CREATE TEMP TABLE tmpimagefile (filename TEXT, imgnum INT, length INT, sha1 TEXT)""")

bfc = con.cursor()
c.execute("""SELECT length, filename, sha1 FROM basefile""")

today = (datetime.date.today().strftime("%Y%m%d"))
if not os.path.exists('./%s' % today): os.mkdir('./%s' % today)

s = requests.Session()
while(true):
	diffound = false
	for ship in ships:
		status = s.get("http://203.104.209.71/kcs/resources/swf/ships/%s.swf" % ship)
		# first if filename is diff length, then double check against others.
		if (status.status_code == 200):
			break
		else:
	if (diffound):
		break
	time.sleep(5)
con.commit()
con.close()
