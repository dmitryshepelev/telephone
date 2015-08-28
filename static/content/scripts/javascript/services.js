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
                result.data[m] = element.attr('value');
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
             cls.prototype.setData = _setData
        }
        if (arguments.length > 1) {
            var data = arguments[1];
            if (!data) {
                if (cls.prototype.hasOwnProperty('getModel')) {
                    var collectedData = _collectModelData(cls.prototype.getModel());
                    data = collectedData.data;
                    instance.creationErrors = collectedData.errors.length > 0 ? collectedData.errors : null
                } else {
                    throw '{0} Class hasn\'t model'.format(errorTitle);
                }
            }
            instance.setData(data);
        }
        return instance
    }
    
    return {
        collectModelData: _collectModelData,
        getParamsString: _getParamsString,
        createInstance: _createInstance
    }
})();