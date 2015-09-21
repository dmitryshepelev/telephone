var Messager = (function () {
    function Message () {
        this._element = {};
        this._id = 'messager';
        this._template = '<div id="' + this._id + '" align="center" style="display: none"></div>';

        this._initElement();
    }

    Message.prototype = {
    	constructor: Message,

        _initElement: function () {
            $('header').prepend(this._template);
            this._element = $('#' + this._id);
            this._element.on('click', this._hide.bind(this));
        },

        _setValues: function (text, type) {
            this._element.addClass('message-' + type);
            this._element.text(text);
        },

        _hide: function () {
            this._element.fadeOut(200, function () {
                this._element.removeClass();
                this._element.text('')
            }.bind(this));
        },

        _show: function (text, type) {
            this._setValues(text, type);
            this._element.fadeIn(200);
        },

        success: function (text) {
            this._show(text, 'success');
        },

        warning: function (text) {
            this._show(text, 'warning');
        },

        error: function (text) {
            this._show(text, 'error');
        },

        info: function (text) {
            this._show(text, 'info');
        }
    };

    return Message;
})();
