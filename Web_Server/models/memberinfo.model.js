const mongoose = require('mongoose');

var MemberinfoSchema = new mongoose.Schema({
   
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


mongoose.model('Memberinfo', MemberinfoSchema);
