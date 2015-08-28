var controller = (function (services) {
    $(document).ready(function () {
        mainController.initTooltips();
        mainController.initRequiredFields()
    });

    var _userPassword = {
        get: function (callback) {
            $.get('/generatePassword/', function (data) {
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
        createMail: function () {
            var mailInstance = services.createInstance(Mail, null);
            if (!mailInstance.creationErrors) {
                mailInstance.createMail();
            } else {
                // TODO: validation error message
            }
        },
        connectDisk: function (event) {
            var diskInstance = services.createInstance(Disk);
            diskInstance.connect();
        },
        createUser: function () {
            var newUserInstance = services.createInstance(NewUser, null);
            console.log(newUserInstance);
        }
    }
})(services);
