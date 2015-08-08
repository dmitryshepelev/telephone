(function () {
    angular.module('factories', [])

        .factory('serviceFactory', ['$http', function ($http) {
            return {
                getSecretKey: function () {
                    return $http.get('/s/key/')
                }
            }
        }])

        .factory('callsFactory', ['$http', function ($http) {
            var _testMode = true;
            // TODO: url to the api
            var baseUrl = _testMode ? '/test' : '';
            return {
                loadCalls: function (params) {
                    return $http.get(baseUrl + params);
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
