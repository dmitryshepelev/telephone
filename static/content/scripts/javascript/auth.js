var auth = (function () {
    var fields = ['username', 'password', 'redirect_url'];
    var errorClass = 'error';

    var getErrorElement = function (errorsArr) {
        var cssClass = 'error-text';
        var errorsHTML = '';
        errorsArr.forEach(function(error) {
            errorsHTML += '<span class="' + cssClass + '">' + error + '</span>';
        });
        return errorsHTML;
    };

    var clearErrorMessages = function () {
        var elements = $('.error');
        for (var i = 0; i < elements.length; i++) {
            elements[i].removeClass(errorClass);
            elements[i].remove()
        }
    };

    return {
        login: function () {
            var formData = {};
            fields.forEach(function (field) {
                formData[field] = $('#' + field)[0].value
            });
            clearErrorMessages();
            $.post('/auth/signin/', formData, function (result) {
                if (result[fields[2]]) {
                    window.location.href = result[fields[2]]
                }
                if (result.errors) {
                    fields.forEach(function(field) {
                        var errorsArr = result.errors[field];
                        if (errorsArr) {
                            var errorElement = $('#' + field);
                            errorElement.parent().append(getErrorElement(errorsArr));
                            errorElement.addClass(errorClass)
                        }
                    });
                }
            })
        }
    }
})();