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
    }
};
