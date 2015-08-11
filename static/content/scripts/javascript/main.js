/**
 * Convert date to string formatted as 'd.m.yyyy'
 * @returns {string}
 */
Date.prototype.toRightDateString = function () {
    var date = [this.getDate(), (this.getMonth() + 1), this.getFullYear()];
    return String(date.join('.'));
};

/**
 * Creates an instance of Date class with current date value
 * @returns {Date}
 */
Date.getNowDate = function () {
    return new Date(Date.now());
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
        // Display anonymous calls: 0 - No; 1 - Yes
        anonymous: 1,
        // New clients only: 0 - No; 1 - Yes
        firstTime: 0,
        // Start date: 'd.m.Y'
        from: Date.getNowDate(),
        // Callee number
        fromNumber: '',
        // Call status: 0 - all calls; 1 - missed; 2 - accepted
        state: 0,
        // End date (inclusively): 'd.m.Y'
        to: Date.getNowDate(),
        // Call responder number
        toAnswer: '',
        // Call destination number
        toNumber: '',
        // Schema number
        tree: '',
        // Call type: 0 - all calls; 1 - incoming; 2 - upcoming; 3 - inner
        type: 0,
        // User code
        user: ''
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

    setTree: function (value) {
        this._params.tree = value;
    },

    setUser: function (value) {
        this._params.user = value;
    },

    setParams: function (params) {
        this._init(params);
    },

    getRequestString: function () {
        var str = '?';
        for (var param in this._params) {
            if (this._params.hasOwnProperty(param)) {
                str += param + '=' + (param === 'from' || param === 'to' ? this._params[param].toRightDateString() :this._params[param]) + '&';
            }
        }
        return str;
    }
};