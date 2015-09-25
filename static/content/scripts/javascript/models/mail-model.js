/**
 * Class represents Mail entity
 * @constructor Mail
 */
function Mail() {
    this._data = {
        login: null,
        password: null
    };
    this._url = '/services/createMail/';
}

Mail.prototype = {
    constructor: Mail,

    /**
     * Returns Mail form fields
     * @returns {{login: string, password: string}}
     */
    getModel: function () {
        return {
            login: 'login',
            password: 'password'
        }
    },
    /**
     * Create request to the server to create new mail
     * @returns JQuery.Deferred
     */
    createMail: function () {
        return $.post(this._url, this._data)
    },

    /**
     * Get mailbox data and update class _data
     * @returns JQuery.Deferred
     */
    getMailboxData: function () {
        return $.get('/services/getMailboxData/', function (data) {
            for (var d in data) {
                if (data.hasOwnProperty(d)) {
                    this._data[d] = data[d]
                }
            }
        }.bind(this))
    },

    /**
     * Fill html fields of class model with _data
     */
    applyModelData: function () {
        var model = this.getModel();
        for (var m in model) {
            if (model.hasOwnProperty(m)) {
                $('#' + model[m]).val(this._data[m]);
            }
        }
    }
};
