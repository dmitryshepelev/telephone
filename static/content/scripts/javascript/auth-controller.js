var auth = (function () {
    services.bindKey('enter', _login);

    function _login() {
        var authInstance = services.createInstance(AuthModel, null);
        if (!authInstance.creationErrors) {
            $.post('/auth/login/', authInstance.getData(), function (result) {
                window.location.href = result['redirect_url'];
            }).fail(function (xhr) {
                var messages = [];
                var errors = JSON.parse(xhr.responseText);
                for (var fieldName in errors) {
                    if (errors.hasOwnProperty(fieldName)) {
                        services.validate(fieldName);
                        var errorText = errors[fieldName];
                        if (messages.indexOf(errorText) == -1) {
                            messages.push(errorText)
                        }
                    }
                }
                message.error(messages.join('; '));
            });
        } else {
            authInstance.creationErrors.forEach(function (errorFieldName) {
                services.validate(errorFieldName);
            });
            message.error('Не все поля заполнены');
        }
    }

    return {
        login: _login
    }
})();