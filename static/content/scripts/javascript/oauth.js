var OAuth = (function (services) {
    function OAuth(onSuccess) {
        this._getTokenSucccesCallback = onSuccess;

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
                        message.error('Token creation error: {0}'.format(errorString))
                    });
                } else {
                    services.validate('oauth-code');
                    message.error('Token creation error: value cannot be null')
                }
            } else {
                message.error('Error: token cannot be get. Mailbox isn\'t created')
            }

        }
    };

    return OAuth;
})(services);