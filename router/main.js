var mysql = require('mysql');

var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '1234',
	database : 'nodejsconnect'
});

var sql = 'SELECT * FROM nodejsconnect.project';

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
});

module.exports = function(app)
{
     app.get('/',function(req,res){
		res.render('list.html',{hitArray,numberArray,nameArray})
     });
	 app.get('/write',function(req,res){
        res.render('write.html')
     });
	 app.post('/result',function(req,res){
        res.render('result.html')
     });
	 app.get('/upload',function(req,res){
        res.render('upload.html')
     });
}