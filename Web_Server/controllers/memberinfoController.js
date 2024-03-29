const express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const Memberinfo = mongoose.model('Memberinfo');
const axios = require('axios');
const memberController = require('./memberController');
const Member = mongoose.model('Member');

// ********* 회원 출입목록 삽입 함수 **********
async function saveExistingMemberToDatabase(existingMember) {
    // 이 부분에서 existingMember를 DB에 저장
    const member = new Member({
        time: existingMember.time,
        fullName: existingMember.fullName,
        pin: existingMember.pin,
        gender: existingMember.gender
        // 다른 필드들도 필요한 경우 여기에 추가
    });

    return new Promise((resolve, reject) => {
        member.save((err, doc) => {
            if (!err) {
                resolve(doc);
            } else {
                reject(err);
            }
        });
    });
}
// ********* 회원 출입목록 삽입 함수 **********


 // ********** 핀번호 확인하는 코드 ********** 
 router.post('/checkMember', async (req, res) => {
    const pinnumber = req.body.pin;
    try {
        const existingMemberinfo = await Memberinfo.findOne({ pin: pinnumber });

        if (existingMemberinfo) { // 해당 핀번호를 가진 회원이 존재하는 경우
            console.log('Memberinfo found:', existingMemberinfo);
            res.send(true);

        } else { // 해당 핀번호를 가진 회원이 존재하지 않는 경우
            console.log('Memberinfo not found for pin:', pinnumber);
            res.send(false);
        }
    } catch (error) {
        console.error('Error checking memberinfo:', error);
        res.status(500).json({ message: 'Internal Server Error' });
    }
});
 // ********** 핀번호 확인하는 코드 **********

 // ********** 이미지 받아서 전송 ************
router.post('/receive', async (req, res) => {
    try {
        // 받은 이미지 데이터와 사용자 ID
        const { Face, Id } = req.body;
    
        // 받은 이미지를 서버에 저장 (옵션)
        //const imagePath = `../uploads/${Id}.png`;
        //const imageBuffer = Buffer.from(Face, 'base64');
        //fs.writeFileSync(imagePath, imageBuffer);
    
        // 서버로 이미지 전송
        const serverUrl = 'http://192.168.0.4:26999/receive';
        const requestData = {
          Face : Face ,
          Id : Id
        };

        const response = await axios.post(serverUrl, requestData);
        // 서버로부터 받은 응답을 클라이언트에 전송
       //res.status(200).json({ success: true, response: response.data });
       res.status(200).send(response.data);
        console.log(response.data);
        if (response.data==true) {
            // 여기에 출입목록 데이터 삽입
            console.log(requestData.Id);

            // requestData.Id의 정보를 가진 Memberinfo 스키마에서 인스턴스를 찾아서 기록
            const existingMember = await Memberinfo.findOne({ pin: requestData.Id });

            console.log(existingMember); // print
            
            
             // 이 부분에서 existingMember를 DB에 저장
             try {
                await saveExistingMemberToDatabase(existingMember);
                console.log('Existing member saved to the database');
            } catch (error) {
                console.error('Error saving existing member to the database:', error);
            } 
        }else{// 신원확인 x
            console.log(`${requestData.Id} 회원 이미지가 일치하지 않음`);

        }
    }  catch (error) {
        console.error('Error:', error);
        res.status(500).json({ success: false, error: 'Internal Server Error' });
      }
      
    });

    


// ********** 이미지 받아서 전송 ************






router.get('/', (req, res) => {
    res.render("memberinfo/addOrEdit", {
        viewTitle: "회원정보"
    });
});

router.post('/', (req, res) => {
    if (req.body._id == '')
        insertRecord(req, res);
        else
        updateRecord(req, res);
});


function insertRecord(req, res) {
    var memberinfo = new Memberinfo();
    memberinfo.fullName = req.body.fullName;
    memberinfo.pin = req.body.pin;
    memberinfo.gender = req.body.gender;
    memberinfo.save((err, doc) => {
        if (!err)
            res.redirect('memberinfo/list');
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("memberinfo/addOrEdit", {
                    viewTitle: "Insert Memberinfo",
                    memberinfo: req.body
                });
            }
            else
                console.log('Error during record insertion : ' + err);
        }
    });
}

function updateRecord(req, res) {
    Memberinfo.findOneAndUpdate({ _id: req.body._id }, req.body, { new: true }, (err, doc) => {
        if (!err) { res.redirect('memberinfo/list'); }
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("memberinfo/addOrEdit", {
                    viewTitle: 'Update Memberinfo',
                    memberinfo: req.body
                });
            }
            else
                console.log('Error during record update : ' + err);
        }
    });
}


router.get('/list', (req, res) => {
    Memberinfo.find((err, docs) => {
        if (!err) {
            res.render("memberinfo/list", {
                list: docs
            });
        }
        else {
            console.log('Error in retrieving memberinfo list :' + err);
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
    Memberinfo.findById(req.params.id, (err, doc) => {
        if (!err) {
            res.render("memberinfo/addOrEdit", {
                viewTitle: "Update Memberinfo",
                memberinfo: doc
            });
        }
    });
});

router.get('/delete/:id', (req, res) => {
    Memberinfo.findByIdAndRemove(req.params.id, (err, doc) => {
        if (!err) {
            res.redirect('/memberinfo/list');
        }
        else { console.log('Error in memberinfo delete :' + err); }
    });
});

module.exports = router;