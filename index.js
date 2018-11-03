const express = require('express');
const app = express();

const port = 3000;

app.use(express.static('public'));
app.use('/js', express.static(__dirname + '/node_modules/matter-js/build/'));
app.use('/js', express.static(__dirname + '/node_modules/pathseg/'));

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
