(function () {
    angular.module('factories', [])

        .factory('callsFactory', ['$http', function ($http) {
            var testMode = true;
            // TODO: url to the api
            var baseUrl = testMode ? '/test/' : '';
            // TODO: params array to request request
            return {
                loadCalls: function () {
                    return $http.get(baseUrl);
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
