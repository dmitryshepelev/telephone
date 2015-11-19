var NewProfileRequestModel = (function () {
    function NewProfileRequestModel () {
    	this._data = {
            login: '',
            email: ''
        };
    }

    NewProfileRequestModel.prototype = {
    	constructor: NewProfileRequestModel,
        getModel: function () {
            return {
                login: 'login',
                email: 'email'
            }
        },
        getData: function () {
            return this._data;
        }
    };

    return NewProfileRequestModel
})();