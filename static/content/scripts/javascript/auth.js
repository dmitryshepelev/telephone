var auth = (function () {
    return {
        login: function (e) {
            var loginFormFields = {
                username: 'username',
                password: 'password',
                redirect_url: 'redirect_url'
            };
            var formData = {};
            for (var field in loginFormFields) {
                if (loginFormFields.hasOwnProperty(field)) {
                    formData[field] = $('#' + field)[0].value
                }
            }
            $.post('/auth/signin/', formData, function (result) {
                if (result[loginFormFields.redirect_url]) {
                    window.location.href = result[loginFormFields.redirect_url]
                }
                if (result.errors) {
                    for (var field in loginFormFields) {
                        if (loginFormFields.hasOwnProperty(field)) {
                            var errorsArray = result.errors[field];
                            var errorElement = $('#' + field);
                            if (errorsArray) {
                                validate.showError(errorElement, validate.getErrorMessageHTML(errorsArray))
                            } else {
                                validate.hideError(errorElement);
                            }
                        }
                    }
                }
            })
        }
    }
})();