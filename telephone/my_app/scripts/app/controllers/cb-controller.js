(function (ng) {

    function _cbCtrl($scope, $apiSrv, toastr, $q, $timeout, $valPBXData) {

        var _numberRE = /^\d{8,14}$/;

        $scope.selfNumber = '';
        $scope.cb = {
            toN: {
                number: '',
                info: {
                    price: 0.0,
                    currency: 'RUB'
                }
            },
            fromN: {
                number: '',
                info: {
                    price: 0.0,
                    currency: 'RUB'
                }
            },
            totalCost: 0,
            getTotalCost: function () {
                return this.totalCost ? Math.floor(this.totalCost * 100) / 100 + ' RUB' : '';
            },
            isReady: false,
            isCalling: false,
            isFormError: false,
            swap: function () {
                var temp = {};
                ng.copy(this.toN, temp);
                ng.copy(this.fromN, this.toN);
                ng.copy(temp, this.fromN);
            },
            setSelfNumber: function () {
                this.fromN.number = $valPBXData.phone;
            },
            call: function () {
                // var self = this;
                // self.isCalling = true;
                // var toastTitle = 'Обратный звонок';
                // $timeout(function () {
                //     $apiSrv.cbCall(self.toN.number, self.fromN.number)
                //         .then(function (response) {
                //             toastr.success('Запрос звонка на номер <strong>' + self.toN.number + '</strong> успешно отправлен', toastTitle);
                //         })
                //         .catch(function () {
                //             toastr.error('Операция временно недоступна. Повторите попытку позже', toastTitle);
                //         })
                //         .then(function () {
                //             self.isCalling = false;
                //         })
                // }, 3000)
            }
        };

        function enableButton() {
            $scope.cb.isReady = _numberRE.test($scope.cb.toN.number) && _numberRE.test($scope.cb.fromN.number);
        }

        function calculateTotalCost() {
            if ($scope.cb.isReady) {
                $scope.cb.totalCost = $scope.cb.toN.info.price + $scope.cb.fromN.info.price; 
            }
        }

        $scope.$watch(
            function () {
                return $scope.cb.toN.number;
            },
            function (newVal, oldVal) {
                if (!_numberRE.test(newVal)) {
                    return 0;
                }
                $apiSrv.getCallCost(newVal)
                    .then(function (result) {
                        $scope.cb.toN.info = result.data.data.call_cost_info;
                        enableButton();
                        calculateTotalCost();
                    })
                    .catch(function(){
                        console.log(arguments);
                    })
            }
        );

        $scope.$watch(
            function () {
                return $scope.cb.fromN.number;
            },
            function (newVal, oldVal) {
                if (!_numberRE.test(newVal)) {
                    return 0;
                }
                $apiSrv.getCallCost(newVal)
                    .then(function (result) {
                        $scope.cb.fromN.info = result.data.data.call_cost_info;
                        enableButton();
                        calculateTotalCost();
                    })
                    .catch(function(){
                        console.log(arguments);
                    })
            }
        );
    }

    _cbCtrl.$inject = ['$scope', '$apiSrv', 'toastr', '$q', '$timeout', '$valPBXData'];

    ng.module('mainApp')
        .controller('CbCtrl', _cbCtrl)

})(angular);
