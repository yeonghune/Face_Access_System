
const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://seung:seung123@mernapp.14zbgex.mongodb.net/myDB', { useNewUrlParser: true, useUnifiedTopology: true}, (err) => {
if (!err) { console.log('MongoDB Connection Succeeded.') }
    else { console.log('Error in DB connection : ' + err) }
});
require('./member.model');
require('./memberinfo.model');
require('./guest.model');