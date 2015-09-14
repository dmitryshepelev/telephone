/**
 * Convert date to string formatted as 'dd.mm.yyyy'
 * @returns {string}
 */
Date.prototype.toRightDateString = function () {
    var day = this.getDate().toString();
    var month = (this.getMonth() + 1).toString();
    var date = [
        day.length < 2 ? '0{0}'.format(day) : day ,
        month.length < 2 ? '0{0}'.format(month) : month,
        this.getFullYear().toString()
    ];
    return String(date.join('.'));
};

/**
 * Creates an instance of Date class with current date value
 * @returns {Date}
 */
Date.getNowDate = function () {
    return new Date(Date.now());
};

/**
 * Extends String prototype with format function. Template: {number}
 * @returns {string}
 */
String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined' ? args[number] : match;
    });
};

function Period(from, to, maxDate) {
    this._maxDate = maxDate || new Date(Date.now());
    this._from = from || new Date(Date.now());
    this._to = to || new Date(Date.now());
}

Period.prototype = {
    constructor: Period,

    getMaxDate: function () {
        return this._maxDate;
    },

    getFromDate: function () {
        return this._from;
    },

    getToDate: function () {
        return this._to;
    },

    setToDate: function (value) {
        if (value instanceof Date) {
            this._to = value;
        } else {
            throw new TypeError('value is not an instance of Date');
        }
    },

    getDatesDifferent: function () {
        var timeDiff = this._to.getTime() - this._from.getTime();
        return Math.ceil(timeDiff / (1000 * 3600 * 24));
    },

    toPeriodString: function (locale) {
        // TODO: Locale
        if (this._from.toDateString() == new Date(Date.now()).toDateString()) {
            return 'сегодня';
        }
        if (this._from.toDateString() == this._to.toDateString()) {
            return this._from.toRightDateString()
        }
        return 'период с ' + this._from.toRightDateString() + ' по ' + this._to.toRightDateString();
    }
};

function ApiParams(params) {
    this._params = {
        // Start date: 'd.m.Y' *Required*
        'start': '',
        // End date (inclusively): 'd.m.Y' *Required*
        'end': '',
        // Determine SIP number
        'sip': '',
        // Wasted cash
        'cost_only': '',
        // Call type: doesn't include - common; 'toll' - 800 number; ru495 - 495 number
        'type': ''
    };

    this._init(params);
}

ApiParams.prototype = {
    constructor: ApiParams,

    _init: function (params) {
        for (var param in params) {
            if (params.hasOwnProperty(param)) {
                this._params[param] = params[param];
            }
        }
    },

    setParams: function (params) {
        this._init(params);
    },

    getRequestString: function () {
        var str = '?';
        for (var param in this._params) {
            if (this._params.hasOwnProperty(param)) {
                str += param + '=' + this._params[param] + '&';
            }
        }
        return str.slice(0, -1);
    }
};


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
        userPassword: null,
        userName: null
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
            userKey: 'user_key',
            secretKey: 'secret_key',
            userEmail: 'user_email',
            userPassword: 'user_password',
            userName: 'user_name'
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