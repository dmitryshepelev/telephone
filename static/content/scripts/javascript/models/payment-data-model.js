/**
 * Class represents payment data model
 * @constructor PaymentData
 */
function PaymentData() {
    this._data = {
        sum: null,
        paymentType: null
    }
}

PaymentData.prototype = {
    constructor: PaymentData,

    /**
     * returns payment data form fields name
     * @returns {{sum: string, paymentType: string}}
     */
    getModel: function () {
        return {
            sum: 'sum',
            paymentType: 'paymentType'
        }
    },

    /**
     * Returns payment data
     * @returns {{sum: null, paymentType: null}|*}
     */
    getData: function () {
        return this._data
    }
};
