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
fulllist = []
with psycopg2.connect(dbname=pgdb, host=pghost, user=pguser, password=pgpass) as fndb:
	with fndb.cursor() as filecur:
		filecur.execute("""SELECT api_filename FROM jsonb_to_recordset((SELECT start2->'api_data'->'api_mst_shipgraph' FROM kcjson ORDER BY apidate DESC LIMIT 1)) a(api_filename TEXT)""")
		for record in filecur:
			fulllist.append(record[0])

con = sqlite3.connect('kcshipimage')
con.execute("""CREATE TABLE IF NOT EXISTS basefile (filename TEXT, length INT, sha1 TEXT)""")
con.execute("""CREATE TABLE IF NOT EXISTS imagefile (filename TEXT, imgnum INT, length INT, sha1 TEXT)""")
con.execute("""CREATE TEMP TABLE IF NOT EXISTS tmpbasefile (filename TEXT, length INT, sha1 TEXT)""")
con.execute("""CREATE TEMP TABLE IF NOT EXISTS tmpimagefile (filename TEXT, imgnum INT, length INT, sha1 TEXT)""")

# test = [[1,"a","3"],[2,"b","5"],[1,"c","7"]]
# ln = {}
# for a in test:
# 	pprint.pprint(a)
# 	if (a[0] in ln):
# 		ln[a[0]] = ln[a[0]] + [(a[1],a[2])]
# 	else:
# 		ln[a[0]] = [(a[1],a[2])]

lengthdict = {}
with con.cursor() as bfc:
	bfc.execute("""SELECT length, filename, sha1 FROM basefile""")
	for record in bfc:
		if(record[0] in lengthdict):
			lengthdict[record[0]] = lengthdict[record[0]] + [(record[1],record[2])]
		else:
			lengthdict[record[0]] = [(record[1],record[2])]

today = (datetime.date.today().strftime("%Y%m%d"))
if not os.path.exists('./%s' % today): os.mkdir('./%s' % today)

s = requests.Session()
while(true):
	diffound = false
	for ship in ships:
		status = s.head("http://203.104.209.71/kcs/resources/swf/ships/%s.swf" % ship)
		# pprint.pprint(vars(status.headers['content-length']))
		# first if filename is diff length, then double check against others.
		if (status.status_code == 200):
			break
		else:
	if (diffound):
		break
	time.sleep(5)
con.commit()
con.close()
