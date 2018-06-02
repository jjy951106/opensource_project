module.exports = function(app)
{
     app.get('/',function(req,res){
        res.render('list.html')
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