const mongoose = require('mongoose');

var GuestSchema = new mongoose.Schema({
    //
    sequence: {
        type: Number,
        default: 0,
        index: true
    },

    time: {
        type: String
    },
    gender: {
        type: String,
        enum: ["남", "여"]
    }
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





GuestSchema.pre('save', function(next) {

    //time
    this.time = Datefunc();

    const doc = this;
    // sequence 필드가 설정되어 있지 않은지 확인
    if (!doc.sequence) {
        
        // 컬렉션에서 최대 sequence 값을 찾아 증가
        mongoose.model('Guest').findOne({}, {}, { sort: { 'sequence': -1 } }, function(err, lastGuest) {
            if (err) {
                return next(err);
            }
            doc.sequence = (lastGuest && lastGuest.sequence || 0) + 1;
            next();
        });
    } else {
        
        next();
    }
});


mongoose.model('Guest', GuestSchema);