var controller = (function () {
    $(document).ready(function () {
        mainController.initTooltips()
    });

    var _mailData = {
        login: 'login',
        email_password: 'email_password'
    };

    var _userPassword = {
        get: function (callback) {
            $.get('/generatePassword/', function (data) {
                callback(data.password)
            })
        },
        set: function (value) {
            $('#password').attr('value', value)
        }
    };

    function _getParamString(data) {
        var str = '';
        for(var d in data) {
            if (data.hasOwnProperty(d)) {
                str += '{0}={1}&'.format(d, data[d])
            }
        }
        return str.slice(0, -1)
    }

    function _createMail(data) {
        var params = _getParamString(data);
        var successElementTemplate = '<span class="pull-right btn btn-lg btn-empty"><span class="glyphicon glyphicon-ok"></span> Почта создана успешно</span>';
        $.get('/createMail?' + params, function (result) {
            $('#uid').attr('value', result.uid);
            $('#createMailBtn').after(successElementTemplate).remove();
        }).fail(function () {

        })
    }

    function _collectFormData(model) {
        var data = {};
        for (var m in model) {
            if(model.hasOwnProperty(m)) {
                data[m] = $('#' + m)[0].value
            }
        }
        return data
    }
    
    return {
        getNewPassword: function () {
            _userPassword.get(_userPassword.set)
        },
        createMail: function () {
            var data = _collectFormData(_mailData);
            _createMail(data);
        }
    }
})();
