const mongoose = require('mongoose');

var Schema = new mongoose.Schema({
   
    time: {
        type: String
    },
    fullName: {
        type: String,
        required: 'This field is required.'
    },
    pin: {
        type: String
    },
    gender: {
        type: String,
        enum: ["남", "여"]
    },    
}, {
    versionKey : false
});

//
function Datefunc() {
    // Format the current date and time as YYYY-MM-DD HH:mm:ss
    const today = new Date();
    const year = today.getFullYear().toString();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    const hours = today.getHours().toString().padStart(2, '0');
    const minutes = today.getMinutes().toString().padStart(2, '0');
    const seconds = today.getSeconds().toString().padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}


// pre-save middleware to update the 'time' field before saving
Schema.pre('save', function (next) {
    this.time = Datefunc();
    next();
});

// Custom validation for email
/*
Schema.path('email').validate((val) => {
    emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return emailRegex.test(val);
}, 'Invalid e-mail.');
*/

mongoose.model('Member', Schema);
