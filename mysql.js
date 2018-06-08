var express = require('express');
var router = express.Router();
var mysql = require('mysql');

var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '1234',
	database : 'nodejsconnect'
});

var sql = 'SELECT * FROM nodejsconnect.project';
//var strArray = sql.split('.');
//console.log(strArray[0]);
var hitArray = new Array();
var numberArray = new Array();
var nameArray = new Array();
var hNum = 0;
var nNum = 0;
var nameNum = 0;

connection.query(sql, function (err, rows) {
  if (err) console.log(err);
  var firstArray = JSON.stringify(rows).split('":');
  for (var i=1; i<firstArray.length; i++){
	  
	  switch (i % 3){
	  case 0:
		hitArray[hNum] = firstArray[i].substring(0,firstArray[i].indexOf("}"));
		hNum++;
		break;
	  case 1:
		numberArray[nNum] = firstArray[i].substring(0,firstArray[i].indexOf(","));
		nNum++;
		break;
	  case 2:
		nameArray[nameNum] = firstArray[i].substring(1,firstArray[i].indexOf("\","));
		nameNum++;
		break;	
	  default:
	  break;
	}
  }
  //var number = firstArray[1].substring(0,firstArray[1].indexOf(","));
  // x%3 == 1 번호
  //var string = firstArray[2].substring(1,firstArray[2].indexOf("\","));
  // x%3 == 2 제품명
  //var hit = firstArray[3].substring(0,firstArray[3].indexOf("}"));
  // x%3 == 0 조회수
  
  for (var i = 0; i<firstArray.length/3-1; i++){
		console.log(hitArray[i]);
		console.log(numberArray[i]);
		console.log(nameArray[i]);
  }
});

router.get('/', function(req, res, next) {
	res.render('list.html',{rows: rows });
});

/*
router.get('/', function(req, res, next) {
	var query = connection.query('select idx,title,writer,hit,DATE_FORMAT(moddate, "%Y/%m/%d %T") as moddate from board',function(err,rows){
    if(err) console.log(err)        // 만약 에러값이 존재한다면 로그에 표시합니다.
    console.log('rows :' +  rows);
    res.render('list', { title:'Board List',rows: rows }); // view 디렉토리에 있는 list 파일로 이동합니다.
  });
});
*/
//module.exports = router;