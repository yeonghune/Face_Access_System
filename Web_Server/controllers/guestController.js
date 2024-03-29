const express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const Guest = mongoose.model('Guest');


// ********* 게스트 출입목록 삽입 함수 **********
async function addGuest(gender) {
    try {
        const newGuest = new Guest({ gender });

        // 새 게스트 항목을 저장합니다.
        await newGuest.save();

        console.log('게스트 항목이 성공적으로 추가되었습니다.');
    } catch (error) {
        console.error('게스트 항목 추가 중 오류 발생:', error.message);
    }
}
// ********* 게스트 출입목록 삽입 함수 **********

// ********* 게스트 출입목록 삽입 컨트롤러 **********
router.post('/addGuest', async(req, res)=>{
    try {
        
        const { gender } = req.body;
        
        

        // 입력된 성별 값으로 게스트 추가
        await addGuest(gender);

        // 성공 응답
        res.status(200).json({ success: true, gender });
    } catch (error) {
        console.error('Error processing /addGuest:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
    }
})
// ********* 게스트 출입목록 삽입 컨트롤러 **********




router.get('/', (req, res) => {
    res.render("guest/addOrEdit", {
        viewTitle: "게스트"
    });
});

router.post('/', (req, res) => {
    if (req.body._id == '')
        insertRecord(req, res);
        else
        updateRecord(req, res);
});


function insertRecord(req, res) {
    var guest = new Guest();
    guest.sequence = req.body.sequence;
    guest.time = req.body.time;
    guest.gender = req.body.gender;
    guest.save((err, doc) => {
        if (!err)
            res.redirect('guest/list');
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("guest/addOrEdit", {
                    viewTitle: "Insert Guest",
                    guest: req.body
                });
            }
            else
                console.log('Error during record insertion : ' + err);
        }
    });
}

function updateRecord(req, res) {
    Guest.findOneAndUpdate({ _id: req.body._id }, req.body, { new: true }, (err, doc) => {
        if (!err) { res.redirect('guest/list'); }
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("guest/addOrEdit", {
                    viewTitle: 'Update Guest',
                    guest: req.body
                });
            }
            else
                console.log('Error during record update : ' + err);
        }
    });
}


router.get('/list', (req, res) => {
    Guest.find((err, docs) => {
        if (!err) {
            res.render("guest/list", {
                list: docs
            });
        }
        else {
            console.log('Error in retrieving guest list :' + err);
        }
    });
});


function handleValidationError(err, body) {
    for (field in err.errors) {
        switch (err.errors[field].path) {
            //
            default:
                break;
        }
    }
}

router.get('/:id', (req, res) => {
    Guest.findById(req.params.id, (err, doc) => {
        if (!err) {
            res.render("guest/addOrEdit", {
                viewTitle: "Update Guest",
                guest: doc
            });
        }
    });
});
router.get('/delete/:id', (req, res) => {
    Guest.findByIdAndRemove(req.params.id, (err, doc) => {
        if (!err) {
            res.redirect('/guest/list');
        }
        else { console.log('Error in guest delete :' + err); }
    });
});

module.exports = router;