(function (ng) {

    function _apiSrv($http) {
        var baseUrl = '/api/';

        return {
            getStat: function (q) {
                var url = baseUrl + 'getstat/' + q || '';
                return $http.get(url);
            }
        }
    }

    _apiSrv.$inject = ['$http'];

    ng.module('mainApp')
        .factory('$apiSrv', _apiSrv)

})(angular);
