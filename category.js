const mongoose = require('mongoose');

const categorySchema = {
    _id: {
        type: String
    },
    parent: {
        type: String,
        ref: 'Category'
    },
    ancestors: [{
        type: String,
        ref: 'Category'
    }]
};

module.exports = new mongoose.Schema(categorySchema);
module.exports.categorySchema = categorySchema;