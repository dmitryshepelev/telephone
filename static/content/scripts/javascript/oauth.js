var OAuth = (function (services) {
    function OAuth(onSuccess) {
        this._getTokenSucccesCallback = onSuccess;
        this._errors = {
            EMBNCR: 'Error: token cannot be get. Mailbox isn\'t created',
            ETOKCR: 'Token creation error: {0}'
        };

        this._initElementsActions()
    }
    OAuth.prototype = {
        constructor: OAuth,

        /**
         * Creates code form in DOM
         */
        _initElementsActions: function () {
            $('#oauth-get-new-code').on('click', this.getOAuthCode.bind(this));
            $('#oauth-send-code').on('click', this.getOAuthToken.bind(this))
        },

        /**
         * Get url and redirect to get code
         */
        getOAuthCode: function () {
            var isMailboxCreated = $('#uid').val() != '';
            if (isMailboxCreated) {
                services.getApiUrls().OAuthCodeUrl().success(function (result) {
                    window.open(result.url, '_blank');
                });
            } else {
                message.error(this._errors.EMBNCR)
            }
        },

        /**
         * Get api access token
         */
        getOAuthToken: function () {
            var isMailboxCreated = $('#uid').val() != '';
            if (isMailboxCreated) {
                var _that = this;
                var value = $('#oauth-code')[0].value;
                if (value) {
                    $.post('/services/getOAuthToken/', { code: value }).success(function (result) {
                        services.executeCallback(_that._getTokenSucccesCallback, result);
                    }).fail(function (xhr) {
                        var errorString = '';
                        if (xhr.responseText) {
                            var data = JSON.parse(xhr.responseText);
                            errorString = '{0}: {1}'.format(data.error, data.error_description);
                        } else {
                            errorString = xhr.statusText;
                        }
                        message.error(_that._errors.ETOKCR.format(errorString))
                    });
                } else {
                    services.validate('oauth-code');
                    message.error(_that._errors.ETOKCR.format('value cannot be null'))
                }
            } else {
                message.error(this._errors.EMBNCR)
            }
        }
    };

    return OAuth;
})(services);