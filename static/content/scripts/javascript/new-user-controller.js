var controller = (function (services) {
    $(document).ready(function () {
        mainController.initTooltips();
        mainController.initRequiredFields();
    });

    var _userPassword = {
        get: function (callback) {
            $.get('/services/generatePassword/', function (data) {
                callback(data.password)
            })
        },
        set: function (value) {
            $('#user_password').attr('value', value)
        }
    };

    return {
        getNewPassword: function () {
            _userPassword.get(_userPassword.set)
        },
        createMail: function (event) {
            var mailInstance = services.createInstance(Mail, null);
            var messageElement = new MessageElement($(event.target), { setMode: 'replace', size: 'lg' });

            if (!mailInstance.creationErrors) {
                loader.show();
                mailInstance.createMail().success(function (result) {
                    $('#uid').attr('value', result.uid);
                    messageElement.success({ message: 'Почта создана успешно' });

                    var tokenContainerElement = $('#token-form-container');
                    var oauth = new OAuth(tokenContainerElement);
                    var tokenMessageElement = new MessageElement(tokenContainerElement, { size: 'lg', position: 'right'});
                    oauth.setGettingTokenCallback(function (result) {
                        $('#token').attr('value', result.access_token);
                        tokenMessageElement.success({ setMode: 'replace', message: 'Токен получен успешно' });
                    }, function () {
                        tokenMessageElement.error({ size: 'sm', setMode: 'append', message: 'Произошла ошибка. Повторите операцию'});
                    });
                    oauth.getOAuthCode();

                }).fail(function () {
                    messageElement.error({ message: 'Операция не завершена' });
                }).done(function () {
                    loader.hide();
                });
            } else {
                $.toaster({ message : mailInstance.creationErrors.join('; '), title: 'Следующие поля не заполнены', priority : 'danger', settings: {timeout: 5000} });
            }
        },
        createUser: function () {
            var newUserInstance = services.createInstance(NewUser, null);
            if (!newUserInstance.creationErrors) {
                loader.show();
                $.post('/admin/newUser/', newUserInstance.getData(), function (result) {
                    window.location.href = '/';
                }).fail(function () {
                    $.toaster({ message : 'Профиль не создан', title: 'Операция не завершена', priority : 'danger', settings: {timeout: 5000} });
                }).done(function () {
                    window.scrollTo(0, 0);
                    loader.hide();
                })
            } else {
                $.toaster({ message : newUserInstance.creationErrors.join('; '), title: 'Следующие поля не заполнены', priority : 'danger', settings: {timeout: 5000} });
            }
        }
    }
})(services);