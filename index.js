const express = require('express');
const app = express();

const http = require('http');
const server = http.createServer(app);
const websocket = require('websocket').server;
const socket = new websocket({httpServer:server});

const port = 3000;

app.use(express.static('public'));
app.use('/js', express.static(__dirname + '/node_modules/matter-js/build/'));
app.use('/js', express.static(__dirname + '/node_modules/pathseg/'));
app.use('/js', express.static(__dirname + '/node_modules/underscore/'));


server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});

socket.on('request', function(request) {
  const connection = request.accept(null, request.origin);
  console.log("hi websocket connection");

  connection.on('message', function(state) {
    console.log(state);
  });

  connection.on('close', function(connection) {
  });
});
