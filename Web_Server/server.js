require('./models/db');
require('dotenv').config();

const PORT = process.env.PORT;
const express = require('express');
const path = require('path');
const exphbs = require('express-handlebars');
const bodyparser = require('body-parser');

const memberController = require('./controllers/memberController');
const guestController = require('./controllers/guestController');
const memberinfoController = require('./controllers/memberinfoController');

var app = express();
app.use(bodyparser.urlencoded({
    extended: true
}));
app.use(bodyparser.json({
    limit:"50mb"
})); 
app.set('views', path.join(__dirname, '/views/'));
app.engine('hbs', exphbs({ extname: 'hbs', defaultLayout: 'mainLayout', layoutsDir: __dirname + '/views/layouts/' }));
app.set('view engine', 'hbs');

app.listen(PORT, () => {
    console.log(`Express server started at port : ${PORT}`);
});

app.use('/member', memberController);
app.use('/memberinfo', memberinfoController);
//add
app.use('/guest', guestController);
app.use('/', memberinfoController);
app.use('/', memberController);
app.use('/', guestController);
