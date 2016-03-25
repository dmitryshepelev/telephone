(function (ng) {

    function _cbCtrl($scope, $apiSrv, toastr, $q) {

        $scope.active = 0;
        $scope.tabs = [
            { idx: 0, activeTitle: 'Кому звоним', title: '1 ', isActive: true, disabled: false, isPassed: false },
            { idx: 1, activeTitle: 'Куда звоним', title: '2', isActive: false, disabled: true, isPassed: false },
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
            $q.all([
                $apiSrv.getCallCost($scope.cb.toN.number),
                $apiSrv.getCallCost($scope.cb.fromN.number)
            ])
                .then(function (result) {
                    $scope.cb.toN.info = result[0].data.info;
                    $scope.cb.fromN.info = result[1].data.info;
                })
                .catch(function () {
                    toastr.error('Неудалось получить данные. Проверьте правильность номеров', 'Обратный звонок')
                })
        }
    }

    _cbCtrl.$inject = ['$scope', '$apiSrv', 'toastr', '$q'];

    ng.module('mainApp')
        .controller('CbCtrl', _cbCtrl)

})(angular);
