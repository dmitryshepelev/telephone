/**
 * Class represents payment data model
 * @constructor SubscribtionData
 */
function SubscribtionData() {
    this._data = {
        receiver: null,
		form_comment: null,
		short_dest: null,
		quickpay_form: null,
		targets: null,
		label: null,
        sum: null,
        paymentType: null,
        duration: null
    }
}

SubscribtionData.prototype = {
    constructor: SubscribtionData,

    /**
     * returns payment data form fields name
     * @returns {{sum: string, paymentType: string}}
     */
    getModel: function () {
        return {
            receiver: 'receiver',
		    form_comment: 'formcomment',
		    short_dest: 'short-dest',
		    quickpay_form: 'quickpay-form',
		    targets: 'targets',
		    label: 'label',
            sum: 'sum',
            paymentType: 'paymentType',
            duration: 'duration'
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
