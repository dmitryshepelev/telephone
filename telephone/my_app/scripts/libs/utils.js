/**
 * Convert date to string formatted as 'dd.mm.yyyy'
 * @returns {string}
 */
Date.prototype.toRightDatetimeString = function () {
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
