var mysql = require('mysql');
var multer = require('multer');
var upload = multer({ dest: './picture/' })
var fs = require('fs');
var path;
var bodyParser = require('body-parser');



var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '1234',
	database : 'nodejsconnect'
});

module.exports = function(app)
{
	app.use(bodyParser.urlencoded({extended: false}));
	app.use(bodyParser.json());
	// list
     app.get('/',function(req,res){
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
		res.render('list.html',{hitArray,numberArray,nameArray})
		});
		
     });
	 app.get('/write',function(req,res){
        res.render('write.html')
     });
	 app.get('/upload',function(req,res,next){
        res.render('upload.html')
     });
	 
	app.get('/board/:id',function(req,res){
		var id = req.params.id;
		
		// 이미지 불러오기 (올린 글에서)
		app.get('/readimg'+id,function (req,res){
			var x = req.params.id;
			connection.query('SELECT path FROM nodejsconnect.photopath WHERE id = '+id,function(err,rows){
				//console.log(rows);
				var pathArray = JSON.stringify(rows).split(':"');
				var realPath = pathArray[1].substring(0,pathArray[1].indexOf("\""));
				//console.log(realPath);
				fs.readFile(realPath,function(err,data){
				res.writeHead(200,{'Content-Type':'text/html'});
				res.end(data);
				});
			});
		});
		
		var hitup = 'UPDATE nodejsconnect.project SET hit = hit + 1 WHERE id = '+id;
		var search = 'SELECT * FROM nodejsconnect.project WHERE id = '+ id;
		connection.query(hitup,function (err){
			if (err) console.log(err);
		});
		connection.query(search, function (err, rows) {
			if (err) console.log(err);
			var readArray = JSON.stringify(rows).split('":');
			var sName = readArray[2].substring(1,readArray[2].indexOf("\","));
			var hit =  readArray[3].substring(0,readArray[3].indexOf("}"));
			res.render('read.html',{id,sName,hit})
		});
	});
	
	app.post('/upload',function(req,res,next){
		var title = req.body.title;
		var id;
		//MAX_VALUE 서치해서 + 1
		connection.query('SELECT MAX(id) FROM nodejsconnect.project',function(err,rows){
			if (err) console.log(err);
			var splitRows = JSON.stringify(rows).split(":");
			id = splitRows[1].substring(0,splitRows[1].indexOf("}"));
			if (id == "null")
				id = 0;
			id = parseInt(id) + 1;
		});
		connection.beginTransaction(function(err) {
			if(err) console.log(err);
			connection.query('INSERT into nodejsconnect.project(id,sName,hit) values(?,?,?)',[id,title,0],function (err) {
				if(err) {
					console.log(err);
					connection.rollback(function () {
						console.error('rollback');
					})
				}
				connection.commit(function (err) {
                if(err) console.log(err);
				});
				res.redirect('/board/'+id);
			})
		})
	});
	
	//업로드 누르기전에 이미 DB에 올라감 여기서 업로드 안하고 나가리되면 DB 꼬이기 시작할거임.
	app.post('/result', upload.single('filetoupload'), function(req,res){
		//파일위치 저장
		path = req.file.path;
		var id;
		//MAX_VALUE 서치해서 + 1
		connection.query('SELECT MAX(id) FROM nodejsconnect.photopath',function(err,rows){
			if (err) console.log(err);
			var splitRows = JSON.stringify(rows).split(":");
			id = splitRows[1].substring(0,splitRows[1].indexOf("}"));
			if (id == "null")
				id = 0;
			id = parseInt(id) + 1;
			//console.log(id);
			connection.query('INSERT into nodejsconnect.photopath(id,path) values(?,?)',[id,path],function (err) {
				if(err) {
					console.log(err);
					connection.rollback(function () {
						console.error('rollback');
					})
				}
				connection.commit(function (err) {
				if(err) console.log(err);
				});
			});
		});
		//console.log(id);
		
		res.render('result.html')
	});
	
	// 업로드한 이미지 보기 (올리기 전)
	app.get('/img',function (req,res){
		fs.readFile(path,function(err,data){
			res.writeHead(200,{'Content-Type':'text/html'});
			res.end(data);
		});
	});
	
}