require('dotenv').config();
const mongoose = require('mongoose');

const MONGODB_URL = process.env.MONGODB_URL;

mongoose.connect(MONGODB_URL, { useNewUrlParser: true, useUnifiedTopology: true}, (err) => {
if (!err) { console.log('MongoDB Connection Succeeded.') }
    else { console.log('Error in DB connection : ' + err) }
});
require('./member.model');
require('./memberinfo.model');
require('./guest.model');