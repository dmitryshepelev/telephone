var mainApp = angular.module('mainApp', ['ui.bootstrap', 'ngAudio', 'filters', 'directives', 'nzToggle', 'controllers']);


mainApp.factory('callsFactory', ['$http' ,function ($http) {
    var testMode = true;
    // TODO: url to the api
    var baseUrl = testMode ? '/test/' : '';
    // TODO: params array to request request
    return {
        loadCalls: function () {
            return $http.get(baseUrl);
        }
    }
}]);