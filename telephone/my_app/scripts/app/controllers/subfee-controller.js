(function (ng) {

    function _sfCtrl($scope, $apiSrv) {

        function SubscriptionOption (monthCount, value, isSelected) {
            this.monthCount = monthCount;
            this.value = value;
            this.isSelected = isSelected || false;
        }

        function initOptions() {
            var subscriptionPaymentStep = 500;
            var labelText = ' мес.';
            var arr = [];
            for (var i = 1; i < 4; i++) {
                arr.push(new SubscriptionOption(i + labelText, i * subscriptionPaymentStep, i == 1));
            }
            arr.push(new SubscriptionOption(6 + labelText, 6 * subscriptionPaymentStep));
            return arr;
        }

        function setSubscriptionPayment(option) {
            if (option instanceof SubscriptionOption) {
                _subscriptionPayment = option.value;
            } else {
                throw TypeError();
            }
        }

        function getSelectedOption() {
            return _options.filter(function (o) {
                return !!o.isSelected;
            })[0];
        }

        function selectOption(option) {
            if (option instanceof SubscriptionOption) {
                var selectedOption = getSelectedOption();
                selectedOption.isSelected = false;
                option.isSelected = true;
                setSubscriptionPayment(option);
            } else {
                throw TypeError();
            }
        }

        var _subscriptionPayment = 0;
        var _options = initOptions();
        setSubscriptionPayment(_options[0]);

        $scope.vm = {
            options: _options,
            selectOption: selectOption,
            selectedOption: getSelectedOption,

            subscribe: function () {

            }
        }

    }

    _sfCtrl.$inject = ['$scope', '$apiSrv'];

    ng.module('mainApp')
        .controller('sfCtrl', _sfCtrl)

})(angular);