var controller = (function (services) {
    $(document).ready(function () {
        mainController.initTooltips();
    });

    var _userPassword = {
        get: function (callback) {
            $.get('/services/generatePassword/', function (data) {
                callback(data.password)
            })
        },
        set: function (value) {
            var element = $('#userPassword');
            element.prop('value', value);
            element.attr('value', value)
        }
    };

    return {
        getNewPassword: function () {
            _userPassword.get(_userPassword.set)
        },
        createMail: function (event) {
            var mailInstance = services.createInstance(Mail, null);
            if (!mailInstance.creationErrors) {
                mailInstance.createMail().success(function (result) {
                    $('#uid').attr('value', result.uid);
                    message.success('Почта создана успешно');
                    var tokenContainerElement = $('#token-form-container');
                    tokenContainerElement.show();
                    var oauth = new OAuth(function (result) {
                        $('#token').attr('value', result.access_token);
                        message.success('Токен успешно получен')
                    });
                }).fail(function (xhr) {
                    message.success('Mailbox creation error: {0}'.format(JSON.parse(xhr.responseText).error));
                }).always(function () {
                    //loader.hide();
                });
            } else {
                mailInstance.creationErrors.forEach(function (errorFieldName) {
                    services.validate(errorFieldName);
                });
                message.error('Не все поля заполнены');
            }
        },
        createUser: function () {
            var newUserInstance = services.createInstance(NewUser, null);
            if (!newUserInstance.creationErrors) {
                loader.show();
                $.post('/admin/newUser/', newUserInstance.getData(), function (result) {
                    if (result.isSuccess) {
                        window.location.href = '/';
                    }
                }).fail(function (xhr) {
                    var errors = [];
                    if (xhr.responseText) {
                        var data = JSON.parse(xhr.responseText);
                        for (var d in data.data) {
                            if (data.data.hasOwnProperty(d)) {
                                errors.push('{0}: {1}'.format(d, data.data[d][0]))
                            }
                        }
                    }
                    message.error(errors.join('\n'));
                }).always(function () {

                })
            } else {
                newUserInstance.creationErrors.forEach(function (errorFieldName) {
                    services.validate(errorFieldName);
                });
                message.error('Не все поля заполнены');
            }
        }
    }
})(services);