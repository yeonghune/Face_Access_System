const express = require('express');
var router = express.Router();
const mongoose = require('mongoose');
const Member = mongoose.model('Member');
const axios = require('axios');
const fs = require('fs');


router.get('/', (req, res) => {
    res.render("member/addOrEdit", {
        viewTitle: "회원"
    });
});

router.post('/', (req, res) => {
    if (req.body._id == '')
        insertRecord(req, res);
        else
        updateRecord(req, res);
});


function insertRecord(req, res) {
    var member = new Member();
    member.time = req.body.time;
    member.fullName = req.body.fullName;
    member.pin = req.body.pin;
    member.gender = req.body.gender;
    member.save((err, doc) => {
        if (!err)
            res.redirect('member/list');
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("member/addOrEdit", {
                    viewTitle: "Insert Member",
                    member: req.body
                });
            }
            else
                console.log('Error during record insertion : ' + err);
        }
    });
}

function updateRecord(req, res) {
    Member.findOneAndUpdate({ _id: req.body._id }, req.body, { new: true }, (err, doc) => {
        if (!err) { res.redirect('member/list'); }
        else {
            if (err.name == 'ValidationError') {
                handleValidationError(err, req.body);
                res.render("member/addOrEdit", {
                    viewTitle: 'Update Member',
                    member: req.body
                });
            }
            else
                console.log('Error during record update : ' + err);
        }
    });
}


router.get('/list', (req, res) => {
    Member.find((err, docs) => {
        if (!err) {
            res.render("member/list", {
                list: docs
            });
        }
        else {
            console.log('Error in retrieving member list :' + err);
        }
    });
});


function handleValidationError(err, body) {
    for (field in err.errors) {
        switch (err.errors[field].path) {
            case 'fullName':
                body['fullNameError'] = err.errors[field].message;
                break;
            default:
                break;
        }
    }
}

router.get('/:id', (req, res) => {
    Member.findById(req.params.id, (err, doc) => {
        if (!err) {
            res.render("member/addOrEdit", {
                viewTitle: "Update Member",
                member: doc
            });
        }
    });
});

router.get('/delete/:id', (req, res) => {
    Member.findByIdAndRemove(req.params.id, (err, doc) => {
        if (!err) {
            res.redirect('/member/list');
        }
        else { console.log('Error in member delete :' + err); }
    });
});

module.exports = router;

