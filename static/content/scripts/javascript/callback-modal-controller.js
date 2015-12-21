(function (services) {
    function _getCallCost (phoneNumber, onSuccess, onFail) {
        if (phoneNumber != '' && phoneNumber.match(/[0-9]{9,}/)) {
            $.get('/getCallCost/?n=' + phoneNumber, function (result) {
                services.executeCallback(onSuccess, result)
            }).fail(function () {
                services.executeCallback(onFail)
            })
        }
    }

    function _onGetCallCostSuccess (result) {
        for (var i in result) {
            if (result.hasOwnProperty(i)) {
                $('#call-info-' + i).text(result[i])
            }
        }
    }

    function _call() {
        var cbToNumber = $('#cbToNumber').val();
        var cbFromNumber = $('#cbFromNumber').val();
        if (cbToNumber == '' || !cbToNumber.match(/[0-9]{9,}/) || cbFromNumber == '' || !cbFromNumber.match(/[0-9]{9,}/)) {
            $('#error.error-text').text('Неправильный номер телефона');
            return false;
        }
        $.get('/requestCallback/?cbFromNumber=' + cbFromNumber + '&cbToNumber=' + cbToNumber)
            .then(function (result) {
                message.success('Запрос отправлен. Ожидайте звонка')
            })
            .fail(function (err) {
                message.error('Произошла ошибка. Повторите попытку');
            }).always(function () {
                $('#modal').modal('toggle');
            })
    }

    $(document).ready(function () {
        var cbToNumberElement = $('#cbToNumber');

        cbToNumberElement.on('blur', function (e) {
            var number = $(this).val();
            _getCallCost(number, _onGetCallCostSuccess);
        });

        var number = cbToNumberElement.val();
        _getCallCost(number, _onGetCallCostSuccess);

        var callbackBtn = $('#callback-call');
        callbackBtn.on('click', function () {
            _call();
        })
    })
})(services);
