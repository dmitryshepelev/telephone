(function (ng) {

    function _cbCtrl($scope, $apiSrv, toastr, $q, $timeout) {

        $scope.active = 0;
        $scope.tabs = [
            { idx: 0, activeTitle: 'Кому звоним', title: '1 ', isActive: true, disabled: false, isPassed: false },
            { idx: 1, activeTitle: 'Откуда звоним', title: '2', isActive: false, disabled: true, isPassed: false },
            { idx: 2, activeTitle: 'Звоним?', title: '3', isActive: false, disabled: true, isPassed: false }
        ];

        $scope.cb = {
            toN: {
                number: '',
                info: {}
            },
            fromN: {
                number: '',
                info: {}
            },
            isCalling: false,
            isFormError: false,
            call: function () {
                var self = this;
                self.isCalling = true;
                var toastTitle = 'Обратный звонок';
                $timeout(function () {
                    $apiSrv.cbCall(self.toN.number, self.fromN.number)
                        .then(function (response) {
                            toastr.success('Запрос звонка на номер <strong>' + self.toN.number + '</strong> успешно отправлен', toastTitle);
                        })
                        .catch(function () {
                            toastr.error('Операция временно недоступна. Повторите попытку позже', toastTitle);
                        })
                        .then(function () {
                            self.isCalling = false;
                        })
                }, 3000)
            }
        };

        $scope.setTab = function (newIdx, oldIdx) {
            var newTab = $scope.tabs[newIdx];
            newTab.isActive = true;
            newTab.disabled = false;
            $scope.active = newIdx;

            var oldTab = $scope.tabs[oldIdx];
            oldTab.isActive = false;
            oldTab.isPassed = true;
        };

        $scope.onThirdTabSelect = function ($event) {
            $scope.cb.isFormError = false;
            $q.all([
                $apiSrv.getCallCost($scope.cb.toN.number),
                $apiSrv.getCallCost($scope.cb.fromN.number)
            ])
                .then(function (result) {
                    $scope.cb.toN.info = result[0].data.info;
                    $scope.cb.fromN.info = result[1].data.info;
                })
                .catch(function () {
                    $scope.cb.isFormError = true;
                    toastr.error('Неудалось получить данные. Проверьте правильность номеров', 'Обратный звонок')
                })
        };
    }

    _cbCtrl.$inject = ['$scope', '$apiSrv', 'toastr', '$q', '$timeout'];

    ng.module('mainApp')
        .controller('CbCtrl', _cbCtrl)

})(angular);
