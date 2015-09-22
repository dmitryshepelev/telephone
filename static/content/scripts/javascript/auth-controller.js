var auth = (function () {
    return {
        login: function (e) {
            var authInstance = services.createInstance(AuthModel, null);
            if (!authInstance.creationErrors) {
                $.post('/auth/login/', authInstance.getData(), function (result) {
                    window.location.href = result['redirect_url'];
                }).fail(function (xhr) {
                    message.error(xhr.responseText);
                });
            } else {
                authInstance.creationErrors.forEach(function (errorFieldName) {
                    services.validate(errorFieldName);
                });
                message.error('Не все поля заполнены');
            }
        }
    }
})();