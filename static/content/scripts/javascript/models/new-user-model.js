/**
 * Class represents NewUser entity
 * @constructor NewUser
 */
function NewUser() {
    this._data = {
        login: null,
        password: null,
        uid: null,
        token: null,
        userKey: null,
        secretKey: null,
        userEmail: null,
        profilePhoneNumber: null,
        userPassword: null,
        userName: null,
        customerNumber: null,
        transactId: null
    }
}

NewUser.prototype = {
    constructor: NewUser,

    /**
     * Return NewUser form fields
     * @returns {{login: string, password: string, uid: string, userKey: string, secretKey: string, userEmail: string, userPassword: string, userName: string}}
     */
    getModel: function () {
        return {
            login: 'login',
            password: 'password',
            uid: 'uid',
            token: 'token',
            userKey: 'userKey',
            secretKey: 'secretKey',
            userEmail: 'userEmail',
            userPassword: 'userPassword',
            profilePhoneNumber: 'profilePhoneNumber',
            userName: 'userName',
            customerNumber: 'customerNumber',
            transactId: 'transactId'
        }
    },

    /**
     * Returns new user's data
     * @returns {{login: null, password: null, uid: null, token: null, userKey: null, secretKey: null, userEmail: null, userPassword: null, userName: null}|*}
     */
    getData: function () {
        return this._data;
    }
};
