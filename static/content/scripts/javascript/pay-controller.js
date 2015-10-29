var controller = (function () {
    var _paymentTypeSelectedClass = 'selected';

    function _changePaymentType (value) {
        var element = $('input[type="hidden"]#paymentType');
        element.val(value)
    }

    function _updatePaymentUI (target) {
        $('.' + _paymentTypeSelectedClass).removeClass(_paymentTypeSelectedClass);
        target.addClass(_paymentTypeSelectedClass);
    }

    function _pay (data) {
        var baseUrl = '/pay/';
        console.log(data);
        return $.post(baseUrl, data);
    }

    $(document).ready(function () {

    });

    return {
        onPaymentTypeChange: function (e) {
            var element = $(e.target);
            if (!element.hasClass(_paymentTypeSelectedClass)) {
                _changePaymentType(element.attr('data-value'));
                _updatePaymentUI(element);
            }
        },
        pay: function () {
            var paymentData = services.createInstance(PaymentData, null);
            if (paymentData.creationErrors) {
                paymentData.creationErrors.forEach(function (errorFieldName) {
                    services.validate(errorFieldName);
                });
                message.error(paymentData.creationErrors.join('; '))
            } else {
                _pay(paymentData.getData())
            }
        }
    }
})();
