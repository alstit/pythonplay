
const path = require('path');
const express = require('express');
const bodyParser= require('body-parser');
const multer = require('multer');
const spawn = require("child_process").spawn;



const app = express();



app.get('/',function(req,res)
{
	console.log("rest is success");
	res.sendFile(__dirname + "/index.html");
});

// SET STORAGE
var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads')
  },
  filename: function (req, file, cb) {
    //cb(null, Date.now() + path.extname(file.originalname));
	cb(null, "input.png");
  }
})
 
var upload = multer({ storage: storage })






app.post('/uploadfile', upload.single('myFile'), (req, res, next) => {
console.log("rest api sucessful");	
  const file = req.file
  if (!file) {
    const error = new Error('Please upload a file')
    error.httpStatusCode = 400
    return next(error)
  }
  
    //res.send(file)
	
	console.log("ready to python ");
	console.log(upload.storage["filename"]);
	const pythonProcess = spawn('python',["./process.py","./uploads/" + "input.png"]);
	pythonProcess.stdout.on('data', function(data) { 
        res.send(data.toString());
    }) ;
	

});





app.get("/processedimage",function(req,res)
{	
	const pythonProcess = spawn('python',["./process.py","./uploads/" ]);
	pythonProcess.stdout.on('data', function(data) { 
        res.send(data.toString());
    }) ;
});



app.listen(3000,()=> console.log("connected on port 3000"))