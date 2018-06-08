var express = require('express');
var app = express();
var router = require('./router/main')(app);
//var board = require('./mysql');

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

var server = app.listen(8080, function(){
    console.log("Server start")
});

//app.use('/',board);