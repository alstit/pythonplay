# pythonplay

python play is a small script using openCV to extract the road of an image and to return a vector to keep a car on the centre of the road 

I have done tests with Dirt Rally and Copa Petrobras de Marcas which is a free game. The image processing are setted up for the Tamura track. 

You can find sample output in /uploads.

Currently the backend python script save image on disk as debug feature. 

you can access the direction vector by request.content after a POST request.

A try to use Nodejs as a REST API to run python commands on a serveur



USAGE: 
npm install
node server.js

go to your client device
pyhton -m pip install -r setup to automatically install requiered packages
python car.py

you can change server addresse directly in python code. 


