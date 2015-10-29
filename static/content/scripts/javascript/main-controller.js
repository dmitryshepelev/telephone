var mainController = (function () {
    function _initTooltips() {
        $('[tooltip]').tooltip();
    }

    function _getAccountBalance () {
        return $.get('/getBalance/')
    }

    function _updateBalanceContainer () {
        var container = $('li.balance-wt');
        if (container) {
            _getAccountBalance().success(function (data) {
                var icon = '<span class="icon-credit-card"></span>';
                container.children('a').text(' {0} {1}'.format(data.balance, data.currency));
                container.children('a').prepend(icon)
            }).error(function () {

            })
        }
    }

    $(document).ready(function () {
        _updateBalanceContainer()
    });

    return {
        initTooltips: _initTooltips
    }
})();