(function (angular) {
    
    function _ValidateSvc() {
        function RequiredValidator (error) {
        	this._error = error;
            this._errorClass = 'warning';
            this._element = angular.element(document.querySelector('[name=' + error.$name + ']'))
        }
        
        RequiredValidator.prototype = {
        	constructor: RequiredValidator,
            setClearanceHandler: function () {
                var self = this;
                if (typeof self._element.oninput !== 'function') {
                    self._element.on('input', function () {
                        var $el = angular.element(this);
                        self.removeError();
                        // make handler to be executed once
                        $el.oninput = undefined;
                    })
                }
            },
            showError: function () {
                this._element.addClass(this._errorClass);
                this.setClearanceHandler();
            },
            removeError: function () {
                this._element.removeClass(this._errorClass);
            },
            getElement: function () {
                return this._element;
            },
            getInfo: function () {
                return {
                    element: this.getElement(),
                    $name: this._error.$name,
                    errorType: 'required'
                }
            }
        };

        var validators = {
            required: RequiredValidator,
            email: RequiredValidator
        };

        var setFocus = function(element) {
            element.focus()
        };

        return {
            validateForm: function (form) {
                var result = {
                    status: true,
                    errors: []
                };

                if (form.$valid) {
                    return result;
                }

                for (var errorType in form.$error) {
                    result.status = false;
                    if (form.$error.hasOwnProperty(errorType)) {
                        console.log(errorType);

                        form.$error[errorType].forEach(function (error) {
                            var validator = new validators[errorType](error);
                            validator.showError();
                            result.errors.push(validator.getInfo())
                        })
                    }
                }

                if (result.errors.length > 0) {
                    setFocus(result.errors[0].element[0]);
                }

                return result;
            }
        }
    }
    
    _ValidateSvc.$inject = [];
    
    angular
        .module('$validator', []);

    angular
        .module('$validator')
        .service('$ValidateSvc', _ValidateSvc)

})(angular);
