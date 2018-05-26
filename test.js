var express = require('express');

var http = require('http');

var app = express();

app.get('/keyboard', function(req, res) {
	
	var data = {
		'type': 'buttons',
		'button': ['안녕']
	};
	
	res.json(data);
});

http.createServer(app).listen(9090, function(){
	console.log('서버 실행');
});