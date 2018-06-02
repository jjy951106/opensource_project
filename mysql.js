var mysql = require('mysql');
var connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : '1234',
	database : 'new_schema'
});

var sql = 'SELECT * FROM new_schema.hwtable';
connection.query(sql, function (err, rows) {
  if (err) console.log(err);
  console.log('rows', rows);
});

connection.end();