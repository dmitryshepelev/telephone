var controller = (function (services) {
    var _tokenContainerElement = null;

    $(document).ready(function () {
        mainController.initTooltips();
        _getNewPassword();
        _getMailboxData();
        _tokenContainerElement = $('#token-form-container');
    });

    function _tokenContainerToggle (toShow) {
        var easeType = 'swing';
        if (toShow) {
            _tokenContainerElement.parent().animate({
                height: 147
            }, 600, easeType, function () {
                _tokenContainerElement.showElement(400);
            });
        } else {
            _tokenContainerElement.hideElement(400, function () {
                _tokenContainerElement.parent().animate({
                    height: 72
                }, 600, easeType)
            });
        }
    }

    function _getNewPassword() {
        _userPassword.get(_userPassword.set);
    }

    function _getMailboxData(onSuccess) {
        var mailboxInstance = services.createInstance(Mail);
        mailboxInstance.getMailboxData().success(function () {
            mailboxInstance.applyModelData();
            services.executeCallback(onSuccess);
        });
    }

    var _userPassword = {
        get: function (callback) {
            $.get('/services/generatePassword/', function (data) {
                callback(data.password)
            })
        },
        set: function (value) {
            var element = $('#userPassword');
            element.val(value);
        }
    };

    return {
        getNewPassword: function () {
            _getNewPassword();
        },
        getMailboxData: function () {
            _getMailboxData(function () {
                $('#uid').attr('value', '');
            });
        },
        createMail: function (event) {
            var mailInstance = services.createInstance(Mail, null);
            if (!mailInstance.creationErrors) {
                loader.show();
                mailInstance.createMail().success(function (result) {
                    $('#uid').attr('value', result.uid);
                    message.success('Почта создана успешно');
                    _tokenContainerToggle(true);
                    var oauth = new OAuth(function (result) {
                        $('#token').attr('value', result.access_token);
                        message.success('Токен успешно получен');
                        _tokenContainerToggle(false);
                    });
                }).fail(function (xhr) {
                    message.error('Mailbox creation error: {0}'.format(JSON.parse(xhr.responseText).error));
                }).always(function () {
                    loader.hide();
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
                $.post('/admin/newuser/', newUserInstance.getData(), function (result) {
                    services.cleanModelData(newUserInstance.getModel(), function () {
                        _getNewPassword();
                        _getMailboxData();
                    });
                    message.success('Пользователь создан успешно');
                    $('html, body').animate({ scrollTop: 0}, 500);
                }).fail(function (xhr) {
                    var errors = [];
                    if (xhr.responseText) {
                        var data = null;
                        try {
                            data = JSON.parse(xhr.responseText);
                            for (var d in data.data) {
                                if (data.data.hasOwnProperty(d)) {
                                    errors.push('{0}: {1}'.format(d, data.data[d][0]))
                                }
                            }
                            message.error(errors.join('\n'));
                        } catch (e) {
                            message.error(xhr.responseText)
                        }
                    }
                }).always(function () {
                    loader.hide();
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