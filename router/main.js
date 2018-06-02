module.exports = function(app)
{
     app.get('/',function(req,res){
        res.render('list.html')
     });
	 app.get('/',function(req,res){
        res.render('write.html')
     });
}