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
        onSubscrChange: function (e) {
            var value = e.target.value;
            var element = $('input#sum[type="hidden"]');
            element.val(value * 500)
        },
        subscribe: function () {
            var subscribtionDataInstance = services.createInstance(SubscribtionData, null);
            if (!subscribtionDataInstance.creationErrors) {
                $.post('/pay/subfee/', subscribtionDataInstance.getData());
                var labelElement = $('input#label[type="hidden"]');
                $.get('/services/getTransactId/', function (data) {
                    labelElement.val(data.id)
                }).fail(function () {
                    labelElement.val('')
                })
            }
        }
    }
})();
