var services = (function () {
    /**
     * Sets data to the '_data' private property of the class.
     * Create new private property '_data' if it doesn't exist
     * @param data to set
     * @private
     */
    function _setData(data) {
        if (!this.hasOwnProperty('_data')) {
            this._data = {};
        }
        for (var d in data) {
            if (data.hasOwnProperty(d)) {
                this._data[d] = data[d]
            }
        }
    }

    /**
     * Collect data from html page based on class model
     * @param model
     * @returns {{data: {}, errors: Array}} data object, array of names of the errors properties
     * @private
     */
    function _collectModelData(model) {
        var result = {
            data: {},
            errors: []
        };
        for (var m in model) {
            if(model.hasOwnProperty(m)) {
                var element = $('#' + model[m]);
                result.data[m] = element[0].value;
                if (!!element.attr('required') && !result.data[m]) {
                    result.errors.push(m)
                }
            }
        }
        return result
    }

    /**
     * Generate params string as 'param1=value&param2=value...' from object
     * @param data
     * @returns {string}
     * @private
     */
    function _getParamsString(data) {
        var str = '';
        for(var d in data) {
            if (data.hasOwnProperty(d)) {
                str += '{0}={1}&'.format(d, data[d])
            }
        }
        return str.slice(0, -1)
    }

    /**
     * Create instance on the class
     * The first argument is class constructor. Required
     * The second argument is data to fill class instance. If the second is missed, class with default values will be created.
     * Else if the second is falsy then data to fill class will be collected form html page based on class model.
     * @returns {cls} instance of cls class
     * @private
     */
    function _createInstance() {
        var errorTitle = 'CrInsErr.';
        var cls = arguments[0];
        var instance = new cls;
        if (!cls.prototype.setData) {
             cls.prototype.setData = _setData;
        }
        if (arguments.length > 1) {
            var data = arguments[1];
            if (!data) {
                if (cls.prototype.hasOwnProperty('getModel')) {
                    var collectedData = _collectModelData(cls.prototype.getModel());
                    data = collectedData.data;
                    instance.creationErrors = collectedData.errors.length > 0 ? collectedData.errors : null
                } else {
                    throw '{0} Class hasn\'t model. Ensure that class \'{1}\' has \'getModel()\' method'.format(errorTitle, cls.name);
                }
            }
            instance.setData(data);
        }
        return instance
    }

    /**
     * Execute callback function with params array
     * @param callback function
     * @param params array
     * @private
     */
    function _executeCallback(callback, params) {
        if (callback) {
            callback(params)
        }
    }

    /**
     * Service to get urls to api access
     * @returns {{OAuthCodeUrl: Function}}
     * @private
     */
    function _getApiUrls() {
        var _baseUrl = '/services/getApiUrls?reason={0}';

        /**
         * Execute GET request to the server
         * @param url
         * @private
         */
        function _executeGetRequest(url) {
            return $.get(url)
        }

        return {
            /**
             * Get url to get OAuth code
             */
            OAuthCodeUrl: function () {
                var url = _baseUrl.format('OAuthCode');
                return _executeGetRequest(url);
            }
        }
    }

    /**
     * Validate html element by its id
     * @param elementId string
     * @param isValid leave undefined or set false value to make element invalid
     * @private
     */
    function _validate (elementId, isValid) {
        var errorCss = 'error';
        var element = $('#' + elementId);
        if (isValid == true) {
            element.removeClass(errorCss);
        } else {
            element.addClass(errorCss);
            element.on('change', _validate.bind(this, elementId, true))
        }
    }

    /**
     * Bind key pressed
     * @param key keyname to bind
     * @param handler to execute
     * @private
     */
    function _bindKey (key, handler) {
        var keyMatch = [
            { name: 'enter', code: 13 }
        ];
        var keyToBind = keyMatch.filter(function (k) {
            return k.name == key
        })[0];
        if (keyToBind) {
            $(document).keypress(function (e) {
                if (e.which == keyToBind.code) {
                    _executeCallback(handler)
                }
            })
        }
    }

    return {
        collectModelData: _collectModelData,
        getParamsString: _getParamsString,
        createInstance: _createInstance,
        executeCallback: _executeCallback,
        getApiUrls: _getApiUrls,
        validate: _validate,
        bindKey: _bindKey
    }
})();