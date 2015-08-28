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
        //// Display anonymous calls: 0 - No; 1 - Yes
        //anonymous: 1,
        //// New clients only: 0 - No; 1 - Yes
        //firstTime: 0,
        //// Start date: 'd.m.Y'
        //from: Date.getNowDate(),
        //// Callee number
        //fromNumber: '',
        //// Call status: 0 - all calls; 1 - missed; 2 - accepted
        //state: 0,
        //// End date (inclusively): 'd.m.Y'
        //to: Date.getNowDate(),
        //// Call responder number
        //toAnswer: '',
        //// Call destination number
        //toNumber: '',
        //// Call type: 0 - all calls; 1 - incoming; 2 - upcoming; 3 - inner
        //type: 0
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
    this._url = '/createMail/';
}

Mail.prototype = {
    constructor: Mail,

    /**
     * Update html
     * @param isSuccess bool, result of operation
     * @param data data to insert
     * @private
     */
    _updateHtml: function (isSuccess, data) {
        var message = new MessageElement({
            position: 'left',
            size: 'lg'
        });
        if (isSuccess) {
            $('#uid').attr('value', data.uid);
            message.setParams({type: 'success', message: 'Почта создана успешно'});
        } else {
            message.setParams({type: 'error', message: 'Операция не завершена'});
        }
        message.setElement($('#createMailBtn'), 'replace');
    },
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
     */
    createMail: function (successCallback) {
        var that = this;
        $.post(this._url, this._data, function (result) {
            that._updateHtml(true, result);
            if (successCallback) {
                successCallback()
            }
        }).fail(function () {
            that._updateHtml(false)
        })
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
            userKey: 'user_key',
            secretKey: 'secret_key',
            userEmail: 'user_email',
            userPassword: 'user_password',
            userName: 'user_name'
        }
    }
};

function Disk() {
    this._templates = {
        connectionForm:
            '<form class="form-horizontal">' +
                '<div class="input-group disk-form btn-group pull-right">' +
                    '<input id="connectDiskCode" style="max-width: 120px" class="form-control" type="text" placeholder="Код" value="">' +
                    '<button id="connectDiskSendCodeBtn" class="btn btn-default" type="button">Подключить</button>' +
                    '<button id="diskGetCode" class="btn btn-default" type="button"><span class="glyphicon glyphicon-repeat"></span></button>' +
                '</div>' +
            '</form>'
    }
}

Disk.prototype = {
    constructor: Disk,

    _getApiUrl: function (reason, successCallback) {
        $.get('/getApiUrls?reason={0}'.format(reason), function (result) {
            window.open(result.url, '_blank');
            if (successCallback) {
                successCallback()
            }
        })
    },
    _getToken: function (code, successCallback) {
        $.post('/getApiToken/', { code: code }, function (result) {
            console.log(result);
            if (successCallback) {
                successCallback()
            }
        })
    },
    getCode: function () {
        this._getApiUrl('code');
    },
    connect: function () {
        var that = this;
        this._getApiUrl('code', function () {
            $('#connectDiskBtn').after(that._templates.connectionForm).remove();
            $('#connectDiskSendCodeBtn').on('click', function (event) {
                var value = $('#connectDiskCode')[0].value;
                if (value) {
                    that._getToken(value)
                }
            });
            $('#diskGetCode').on('click', function () {
                that._getApiUrl('code');
            })
        })
    }
};

function MessageElement(params) {
    this._template = '<span class="pull-{0} {1} btn-empty btn-padding-0 {2}-message"><span class="glyphicon glyphicon-{3}"></span> {4}</span>'
    this._params = {
        position: 'left',
        size: '',
        type: '',
        icon: '',
        message: ''
    };
    this.setParams(params);
}

MessageElement.prototype = {
    constructor: MessageElement,

    setParams: function (params) {
        for (var p in params) {
            if (params.hasOwnProperty(p)) {
                this._params[p] = params[p]
            }
        }
    },
    setElement: function (element, mode) {
        var messageElement = this.getElement();
        if (mode === 'replace') {
            element.after(messageElement).remove()
        } else {
            element[mode](messageElement)
        }
    },
    getElement: function () {
        var position = this._params.position;
        var size = this._params.size ? 'btn-' + this._params.size : '';
        var type = this._params.type || 'success';
        var icon = type === 'success' ? 'ok' : 'remove';
        var message = this._params.message || type;
        return this._template.format(position, size, type, icon,message);
    }
};