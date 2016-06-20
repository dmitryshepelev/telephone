(function (angular) {

    function CommonService() {
        return {
            /**
             * Extends parent
             * @param base
             * @param child
             */
            extendBase: function (base, child) {
                var F = function () {};
                F.prototype = base.prototype;
                child.prototype = new F();
                child.prototype.constructor = child;
                child.super = base.prototype;
            },
            /**
             * Build query string from object
             */
            encodeQueryData: function (data) {
                if (typeof data !== 'object' || Array.isArray(data) || data === null) {
                    throw new TypeError('The parameter \'data\' is not an object')

                } else {
                    var strings = [];

                    for (var d in data) {
                        if (data.hasOwnProperty(d) && data[d] !== '') {
                            strings.push(d + '=' + data[d])
                        }
                    }

                    return strings.join('&');
                }
            },
            /**
             * Returns query string from params
             * @param params
             * @param defaultParams
             * @returns {string}
             */
            getQueryStringFromParams: function (params, defaultParams) {
                defaultParams = defaultParams || {};
                params = params || {};
                if (angular.isObject(params)) {
                    angular.extend(defaultParams, params)
                } else {
                    throw new TypeError('The parameter \'params\' is not an object')
                }
                var paramsString = this.encodeQueryData(defaultParams); 
                return paramsString ? '?' + paramsString : '';
            },
            /**
             * Creates flat copy of object
             * @param obj
             * @returns {{}}
             */
            createFlatCopy: function (obj) {
                var copy = {};
                angular.copy(obj, copy);
                for (var prop in copy) {
                    if (copy.hasOwnProperty(prop) && typeof copy[prop] === 'object' && copy[prop].hasOwnProperty('guid')) {
                        copy[prop + '_id'] = copy[prop].guid;
                        delete copy[prop];
                    }
                }
                return copy;
            },
            /**
             * Get instance index in array
             * Default field name - 'guid'
             */
            getIndexByField: function (array, fieldValue, fieldName) {
                fieldName = fieldName || 'guid';
                
                if (!fieldValue) {
                    throw new Error('Field value must be defined')
                }
                
                var obj = array.filter(function (item) {
                    return item[fieldName] === fieldValue;
                });
                
                if (obj.length > 1) {
                    throw new Error('Multiple objects found');
                }
                return obj.length == 1 ? array.indexOf(obj[0]) : -1;
            }
        }
    }

    CommonService.$inject = [];

    angular
        .module('mainApp')
        .service('$commonSrv', CommonService)

})(angular);

