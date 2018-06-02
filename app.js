var express = require('express');
var path = require('path');


var index = require('./routes/index');
var users = require('./routes/users');
var board = require('./routes/board');    //board 파일 등록


var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use('/', index);
app.use('/users', users);
app.use('/board',board);        //app에 등록합 /board로 접속요청이 들어왔을때 board 파일로 이동시켜 줌