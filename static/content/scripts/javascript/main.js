Date.prototype.toRightDateString = function () {
    var date = [this.getDate(), (this.getMonth() + 1), this.getFullYear()];
    return String(date.join('.'));
};

var Period = function(from, to, maxDate) {
    this._maxDate = maxDate || new Date(Date.now());
    this._from = from || new Date(Date.now());
    this._to = to || new Date(Date.now());

    this.getMaxDate = function () {
        return this._maxDate;
    };

    this.getFromDate = function () {
        return this._from;
    };

    this.getToDate = function () {
        return this._to;
    };

    this.toPeriodString = function (locale) {
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