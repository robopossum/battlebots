

const express = require('express');
const app = express();
const uid = require('uuid/v1');

const http = require('http');
const server = http.createServer(app);
const websocket = require('websocket').server;
const socket = new websocket({httpServer:server});

const port = 3001;

app.use(express.static('public'));
app.use('/js', express.static(__dirname + '/node_modules/matter-js/build/'));
app.use('/js', express.static(__dirname + '/node_modules/pathseg/'));
app.use('/js', express.static(__dirname + '/node_modules/underscore/'));


server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});



socket.on('request', function(request) {
  const connection = request.accept(null, request.origin);
  var sessionID = uid();

  console.log("hi websocket connection");
  console.log(sessionID);
  console.log(Date.now());

	var world = require('./public/js/world.js');
	var raycast = require("./public/js/raycast.js");
	var agent = require("./public/js/agent.js");
	var xp = require("./public/js/xp.js");
	var shot = require("./public/js/shot.js");
	var keys = require("./public/js/key-controller.js");
	var dummy = require("./public/js/dummy-controller.js");


	var Matter = require( "./node_modules/matter-js");



	var game = {};
	game = new world(2000, 1200, false);
	var agent = new agent(400, 300, new keys(), game.engine, connection);

	//console.log();
	game.spawnXp(100);
	//game.run();
	
  connection.sendUTF(
  	JSON.stringify({ type:'id', data: sessionID}));

  connection.on('message', function(action) {
    //console.log("This is in the main object");
	action = (JSON.parse(action.utf8Data).data);
	inputs = {
	            up: false,
	            down: false,
	            left: false,
	            right: false,
	            turnLeft: false,
	            turnRight: false,
	            shoot: false
	        };


	for(var idx in action) {
	  var item = action[idx];
	  inputs[idx] = item;
	}

	//console.log("now we get the new state");
	state = (runIteration(game, agent, inputs));
 	
 	connection.sendUTF(
 		JSON.stringify(state));
 });
 	// here we need to pass the action into the iterate function

  connection.on('close', function(connection) {
  });
});


//import world from './public/js/world.js';





runIteration  = function(game, agent, actions) {
	agent.controller.inputs = inputs
	game.iterate(game.engine, [delta=16.666], [correction=1]);
	return (agent.iterate(100));
}


 //        <script type="text/javascript" src="js/matter.min.js"></script>
 //        <script type="text/javascript" src="js/pathseg.js"></script>
 //        <script type="text/javascript" src="js/underscore-min.js"></script>
 //        <script type="text/javascript" src="js/raycast.js"></script>
 //        <script type="text/javascript" src="js/agent.js"></script>
 //        <script type="text/javascript" src="js/xp.js"></script>
 //        <script type="text/javascript" src="js/shot.js"></script>
 //        <script type="text/javascript" src="js/key-controller.js"></script>
	// <script type="text/javascript" src="js/dummy-controller.js"></script>
	// <script type="text/javascript">
 //        <script type="text/javascript" src="js/dummy-controller.js"></script>
 //        <script type="text/javascript" src="js/world.js"></script>
 //        <script type="text/javascript">w
