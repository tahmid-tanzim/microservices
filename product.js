const mongoose = require('mongoose');
const Category = require('./category');
const fx = require('./fx');

const productSchema = {
    name: {
        type: String,
        required: true
    },
    pictures: [{
        type: String,
        match: /^http:\/\//i
    }],
    price: {
        amount: {
            type: Number,
            required: true,
            set(v) {
                this.internal.approximatePriceUSD = v / (fx()[this.price.currency] || 1);
                return v;
            }
        },
        currency: {
            type: String,
            enum: ['USD', 'EUR', 'GBP'],
            required: true,
            set(v) {
                this.internal.approximatePriceUSD = this.price.amount / (fx()[v] || 1);
                return v;
            }
        }
    },
    category: Category.categorySchema,
    internal: {
        approximatePriceUSD: Number
    }
};

var schema = new mongoose.Schema(productSchema);

var currencySymbols = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
};

schema.virtual('displayPrice').get(function () {
   return currencySymbols[this.price.currency] + '' + this.price.amount;
});

schema.set('toObject', {virtuals: true});
schema.set('toJSON', {virtuals: true});

module .exports = schema;