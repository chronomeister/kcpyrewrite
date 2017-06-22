const fs = require('fs');
const readline = require('readline');
const req = require('request');
const ships = require('./shipnamemapping.json');

var keys = [2475, 6547, 1471, 8691, 7847, 3595, 1767, 3311, 2507, 9651, 5321, 4473, 7117, 5947, 9489, 2669, 8741, 6149, 1301, 7297, 2975, 6413, 8391, 9705, 2243, 2091, 4231, 3107, 9499, 4205, 6013, 3393, 6401, 6985, 3683, 9447, 3287, 5181, 7587, 9353, 2135, 4947, 5405, 5223, 9457, 5767, 9265, 8191, 3927, 3061, 2805, 3273, 7331];
var servers = ["203.104.209.71", "203.104.209.87", "125.6.184.16", "125.6.187.205", "125.6.187.229", "125.6.187.253", "125.6.188.25", "203.104.248.135", "125.6.189.7", "125.6.189.39", "125.6.189.71", "125.6.189.103", "125.6.189.135", "125.6.189.167", "125.6.189.215", "125.6.189.247", "203.104.209.23", "203.104.209.39"];

var readin = readline.createInterface({
	input : fs.createReadStream('./togetships.txt')
});

var toget = [];
readin.on('line', (ship) => {
	toget.push(ship);
});
readin.on('close', () => {
	toget.forEach(function(findname){
		//
		var shipobj = ships.find(function(elm){
			return elm.name == this;
		}, findname);
		if (!shipobj) {console.log(`No matching name for ${findname}`); return;}
		let dirs = [];
		let mkd = new Promise((mrs, mrj) => {fs.mkdir(`./${findname}`, () => {mrs();});});

		await mkd.then(()=>{
			let lines = [];
			for (let i = 1; i < 53; i++) {
				var filename = (100000 + (17 * (shipobj.api_id + 7) * (keys[i - 1]) % 99173));
				var server = servers[Math.floor(Math.random() * servers.length)];
				let line = new Promise((res,rej) => {
					req({url:`http://${server}/kcs/sound/kc${shipobj.api_filename}/${filename}.mp3`}, (err, rsp, bod) => {
						// console.log(rsp.statusCode);
						fs.writeFile(`./${findname}/${i}.mp3`, bod, () => {res();});
					});
				});
				lines.push(line);
				// console.log(`http://${server}/kcs/sound/kc${shipobj.api_filename}/${filename}.mp3`);
			}
			console.log(`${findname} is started!`);
			Promise.all(lines).then(()=>{console.log(`${findname} is done!`);});
		});
	});
})

/*

with open("./togetships.txt", "r") as getships:
	for line in getships:
		line = line.rstrip()
		print(line)
		if (nametoid[line] == None):
			print("Could not find %s".format(line))
		else:
			shipstoget.append(line)
for ship in shipstoget:
	id = nametoid[ship]
	filename = idtofile[id]
	os.makedirs("./%s" % (ship), exist_ok=True)
	for i in range(53):
		fn = str(100000 + (17 * (int(id) + 7) * int(keys[i + 1] - keys[i])) % 99173)
		url = "http://%s/kcs/sound/kc%s/%s.mp3" % (random.choice(servers), idtofile[id], fn)
		rsp = requests.get(url)
		if (rsp.status_code == 200):
			with open("./%s/%s.mp3" % (ship, i), "wb") as voice:
				voice.write(rsp.content)
			print("200 : %s : %s : %s" % (ship, i, fn))

		# elif (i == 5):
			# print("%s : %s : %s" % (rsp.status_code, ship, i))
		else:
			print("%s : %s : %s : %s" % (rsp.status_code, ship, i, fn))
			# break
*/
