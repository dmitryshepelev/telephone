(function () {
    angular.module('factories', [])

        .factory('callsFactory', ['$http', function ($http) {
            var _getParamsString = function (params) {
                var str = '?';
                for (var p in params) {
                    if (params.hasOwnProperty(p)) {
                        str += p + '=' + params[p] + '&';
                    }
                }
                return str.slice(0, -1);
            };
            var _testMode = true;
            // TODO: url to the api
            var baseUrl = _testMode ? '/test' : '';
            // TODO: params array to request request
            return {
                loadCalls: function (params) {
                    return $http.get(baseUrl + _getParamsString(params));
                }
            }
        }])

        .factory('modalsProvider', ['$modal', function ($modal) {
            return {
                periodModal: function (resolveObj, resultFn) {
                    $modal.open({
                        animation: true,
                        templateUrl: 'get_period_modal_template',
                        controller: 'periodModalCtrl',
                        resolve: {
                            period: function () {
                                return resolveObj.period;
                            }
                        }
                    }).result.then(resultFn);
                }
            }
        }]);
})();
