(function (ng) {

    function _titleCtrl($scope, $titleSrv) {
        $scope.title = $titleSrv.getTitle;
    }

    _titleCtrl.$inject = ['$scope', '$titleSrv'];

    ng.module('mainApp')
        .controller('TitleCtrl', _titleCtrl)

})(angular);
