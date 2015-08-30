var MessageElement = (function ($) {
    /**
     * Message element class
     * @param element JQuery element
     * @param params object
     * @constructor MessageElement
     */
    function MessageElement (element, params) {
        this._element = element;
        this._template = '<span class="pull-{0} {1} btn-empty btn-padding-0 {2}-message"><span class="glyphicon glyphicon-{3}"></span> {4}</span>'
        this._types = {
            success: 'success',
            error: 'error'
        };
        this._params = {
            position: 'left',
            size: '',
            icon: '',
            message: '',
            setMode: 'append'
        };
        this.setParams(params);
    }

    MessageElement.prototype = {
        constructor: MessageElement,

        /**
         * Merge params objects. Options object has higher priority
         * @param defaults params object
         * @param options params object
         * @returns {*}
         * @private
         */
        _mergeParams: function (defaults, options) {
            return $.extend({}, defaults, options);
        },

        /**
         * Return ready to render html template
         * @param type of the message. this._types value
         * @returns {string} html template
         * @private
         */
        _getTemplate: function (type) {
            var size = this._params.size ? 'btn-' + this._params.size : '';
            var message = this._params.message || type;
            return this._template.format(this._params.position, size, type, this._params.icon, message);
        },

        /**
         * Creates message DOM element
         * @param type of the message. this._types value
         * @private
         */
        _render: function (type) {
            var messageElement = this._getTemplate(type);
            if (this._params.setMode === 'replace') {
                this._element.after(messageElement).remove()
            } else {
                this._element[this._params.setMode](messageElement)
            }
        },

        /**
         * Set class params
         * @param params object
         */
        setParams: function (params) {
            for (var p in params) {
                if (params.hasOwnProperty(p)) {
                    this._params[p] = params[p]
                }
            }
        },

        /**
         * Creates success message element
         * @param params object
         */
        success: function (params) {
            this.setParams(this._mergeParams({icon: 'ok'}, params));
            this._render(this._types.success);
        },

        /**
         * Creates error message element
         * @param params object
         */
        error: function (params) {
            this.setParams(this._mergeParams({icon: 'remove'}, params));
            this._render(this._types.error);
        }
    };

    return MessageElement
})($);