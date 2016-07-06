(function (ng) {

    function _apiSrv($http, $commonSrv) {
        var baseUrl = '/api/';

        return {
            getStat: function (params) {
                var defaultParams = {
                    start: new Date().getTime(),
                    end: new Date().getTime(),
                    status: 0,
                    call_type: ''
                };
                var queryString = $commonSrv.getQueryStringFromParams(params || {}, defaultParams);
                var url = baseUrl + 'getstat/' + queryString;
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
                return $http.get(baseUrl + 'getpbxinfo/');
            },
            downloadCRUrl: baseUrl + 'getcrfile/?cid=',
            getCallRecordFile: function (callId) {
                return $http.get(this.downloadCRUrl + callId);
            }
        }
    }

    _apiSrv.$inject = ['$http', '$commonSrv'];

    ng.module('mainApp')
        .factory('$apiSrv', _apiSrv)

})(angular);
