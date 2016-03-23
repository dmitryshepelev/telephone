(function (ng) {

    function _apiSrv($http) {
        var baseUrl = '/api/';

        return {
            getStat: function () {
                var url = baseUrl + 'getstat/';
                return $http.get(url);
            }
        }
    }

    _apiSrv.$inject = ['$http'];

    ng.module('mainApp')
        .factory('$apiSrv', _apiSrv)

})(angular);
