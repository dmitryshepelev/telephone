(function (ng) {

    function _wsCtrl($scope, $apiSrv, $sce) {

        $scope.vm = {
            data: {
                counterNumber: '',
                scriptCode: ''
            },
            getScript: getScript
        };

        function getScript() {
            var self = this;
            $apiSrv.getWsScript(this.data.counterNumber)
                .then(function (result) {
                    self.data.scriptCode = $sce.trustAsHtml(result.data.data.ws);
                })
                .catch(function (error) {

                })
        }

    }

    _wsCtrl.$inject = ['$scope', '$apiSrv', '$sce'];

    ng.module('mainApp')
        .controller('wsCtrl', _wsCtrl)

})(angular);