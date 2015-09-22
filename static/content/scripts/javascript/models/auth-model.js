var AuthModel = (function () {
    function AuthModel () {
    	this._data = {
            username: '',
            password: '',
            redirect_url: ''
        };
    }

    AuthModel.prototype = {
    	constructor: AuthModel,
        getModel: function () {
            return {
                username: 'username',
                password: 'password',
                redirect_url: 'redirect_url'
            }
        },
        getData: function () {
            return this._data;
        }
    };

    return AuthModel
})();
