(function (ng) {

    function _sfCtrl($scope, $apiSrv) {

        $scope.vm = {


            subscribe: function () {

            }
        }

    }

    _sfCtrl.$inject = ['$scope', '$apiSrv'];

    ng.module('mainApp')
        .controller('sfCtrl', _sfCtrl)

})(angular);