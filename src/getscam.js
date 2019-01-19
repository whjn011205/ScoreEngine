request = require('request');
fs = require('fs')

saveJson = (object, dirName = './Data/', fileName) => {
	if (!fs.existsSync(dirName))
		new Promise(res => {
			mkdirp(dirName, async err => {
				if (err) {
					util.logError(err);
					res(false);
				} else {
					util.logInfo(`${dirName} created`);
					res(true);
				}
			});
		});
	return new Promise(res => {
		fs.writeFile(
			dirName + '/' + fileName,
			JSON.stringify(object, null, 4),
			{
				flag: 'w+'
			},
			err => {
				if (err) {
					res(false);
				} else {
					// util.logDebug( `File saved at ${dirName + '/' + fileName}`);
					res(true);
				}
			}
		);
	})
		.then(() => true)
		.catch(err => {
			util.logError( err);
			return false;
		});
};

result = new Promise((resolve, reject) => {
	request(
		{
			url: 'https://etherscamdb.info/api/addresses/',
			method: 'GET'
		},
		(err, res, body) => {
			if (err) reject(err);
			else if (res.statusCode === 200) resolve(body);
			else reject('Error status: ' + res.statusCode + '' + res.statusMessage);
		}
	);
}).then(x => {
    x = JSON.parse(x);
    saveJson(x,'./','etherscamdb.json')
});
