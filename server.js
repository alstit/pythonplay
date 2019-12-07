
const path = require('path');
const express = require('express');
const bodyParser= require('body-parser');
const multer = require('multer');
const spawn = require("child_process").spawn;



const app = express();

//SET STORAGE
// var storage = multer.diskStorage({
  // destination: function (req, file, cb) {
    // cb(null, 'uploads')
  // },
  // filename: function (req, file, cb) {
    ////cb(null, Date.now() + path.extname(file.originalname));
	// cb(null, "input.png");
  // }
// })

var storage = multer.memoryStorage()

 
var upload = multer({ storage: storage })

app.post('/uploadfile', upload.single('myFile'), (req, res, next) => {
	console.log(req.file.buffer);
	
	const pythonProcess = spawn('python',["./process.py"]);
	pythonProcess.stdin.write(req.file.buffer);
	pythonProcess.stdin.end();
	
	pythonProcess.stderr.on('data',function(data)
	{
		console.log(data.toString());
	});
	
	pythonProcess.stdout.on('data', function(data) { 
        res.end(data);
    }) ;
		
});

/*app.get("/processedimage",function(req,res)
{	
	const pythonProcess = spawn('python',["./process.py","./uploads/" ]);
	pythonProcess.stdout.on('data', function(data) { 
        res.send(data.toString());
    }) ;
});*/



app.listen(3000,()=> console.log("connected on port 3000"))
