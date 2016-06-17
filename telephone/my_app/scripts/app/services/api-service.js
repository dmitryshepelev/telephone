(function (ng) {

    function _apiSrv($http) {
        var baseUrl = '/api/';

        return {
            getStat: function (q) {
                var url = baseUrl + 'getstat/' + q || '';
                return $http.get(url);
            },
            getCallCost: function (n) {
                n = n && n[0] === '+' ? n.slice(1) : n;
                var url = baseUrl + 'getcallcost/?n=' + n;
                return $http.get(url);
            },
            cbCall: function (toN, fromN) {
                toN = toN.toString();
                fromN = fromN ? fromN.toString() : '';
                var url = baseUrl + 'cbcall/?fromN=' + fromN + '&toN=' + toN;
                return $http.get(url)
            },
            getCostByCountry: function (country) {
                var url = baseUrl + 'getcostbycountry/?country=' + country;
                return $http.get(url);
            },
            getPBXinfo: function () {
                return $http.get(baseUrl + 'get_pbx_info/');
            }
        }
    }

    _apiSrv.$inject = ['$http'];

    ng.module('mainApp')
        .factory('$apiSrv', _apiSrv)

})(angular);
