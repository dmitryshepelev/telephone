var OAuth = (function (services) {
    function OAuth(element) {
        this._element = element;
        this._getTokenSucccesCallback = null;
        this._getTokenErrorCallback = null;
        this._templates = {
            codeForm:
                '<form id="oauth-code-form" class="form-horizontal">' +
                    '<div class="input-group disk-form btn-group pull-right">' +
                        '<input id="oauth-code" style="max-width: 120px" class="form-control" type="text" placeholder="Код" value="">' +
                        '<button id="oauth-send-code" class="btn btn-default" type="button">Получить токен</button>' +
                        '<button id="oauth-get-new-code" class="btn btn-default" type="button"><span class="glyphicon glyphicon-repeat"></span></button>' +
                    '</div>' +
                '</form>'
        };
        this.initCodeForm();
    }
    OAuth.prototype = {
        constructor: OAuth,

        /**
         * Creates code form in DOM
         */
        initCodeForm: function () {
            this._element.append(this._templates.codeForm);
            $('#oauth-get-new-code').on('click', this.getOAuthCode.bind(this));
            $('#oauth-send-code').on('click', this.getOAuthToken.bind(this))
        },

        /**
         * Sets events callbacks
         * @param success
         * @param error
         */
        setGettingTokenCallback: function (success, error) {
            this._getTokenSucccesCallback = success || null;
            this._getTokenErrorCallback = error || null;
        },

        /**
         * Get url and redirect to get code
         */
        getOAuthCode: function () {
            services.getApiUrls().OAuthCodeUrl().success(function (result) {
                window.open(result.url, '_blank');
            });
        },

        /**
         * Get api access token
         */
        getOAuthToken: function () {
            var _that = this;
            var value = $('#oauth-code')[0].value;
            if (value) {
                $.post('/services/getOAuthToken/', { code: value }).success(function (result) {
                    services.executeCallback(_that._getTokenSucccesCallback, result);
                }).fail(function () {
                    services.executeCallback(_that._getTokenErrorCallback);
                });
            }
        }
    };

    return OAuth;
})(services);
