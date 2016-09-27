(function (ng) {

    function _blcCtrl($scope, $apiSrv) {

        $scope.vm = {

            data: {
                sum: ''
            },
            subscribe: function () {

            }
        }

    }

    _blcCtrl.$inject = ['$scope', '$apiSrv'];

    ng.module('mainApp')
        .controller('blcCtrl', _blcCtrl)

})(angular);