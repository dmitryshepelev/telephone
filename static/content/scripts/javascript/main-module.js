var mainApp = angular.module('mainApp', []);


mainApp.filter('fromSeconds', function () {
    return function(value) {
        var min = Math.floor(value / 60);
        var sec = value - min * 60;
        return (min > 0 ? min + ' мин ' : '') + (sec < 10 ? '0' + sec : sec) + ' сек';
    }
})


mainApp.factory('callsFactory', ['$http' ,function ($http) {
    var testMode = true;
    // TODO: url to the api
    var baseUrl = testMode ? '/test/' : '';
    // TODO: params array to request request
    return {
        loadCalls: function () {
            var url = baseUrl;
            return $http.get(url);
        }
    }
}]);


mainApp.controller('ctrl', ['$scope', 'callsFactory', function ($scope, callsFactory) {
    $scope.calls = [];

    callsFactory.loadCalls().success(function (data) {
        if (data) {
            $scope.calls = converter.csv_to_json(data);
            console.log($scope.calls);
        } else {
            throw 'Empty Response';
        }
    })
}]);