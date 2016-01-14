const mongoose = require('mongoose');
const schema = require('./schema');

mongoose.connect('mongodb://localhost:27017/test');

/* Parameters are: model name, schema, collection name */
var User = mongoose.model('User', schema, 'users');

var user = new User({
    name: 'Tahmid Tanzim',
    email: 'tahmid.tanzim@gmail.com'
});

user.save(error => {
    if(error) {
        console.log(error);
        process.exit(1);
    }

    User.find({email: 'tahmid.tanzim@gmail.com'}, (error, docs) => {
        if(error) {
            console.log(error);
            process.exit(1);
        }
        console.log(require('util').inspect(docs));
        process.exit(0);
    });
});