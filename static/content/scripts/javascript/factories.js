(function () {
    angular.module('factories', [])

        .factory('callsFactory', ['$http', function ($http) {
            return {
                loadCalls: function (params) {
                    return $http.get('/getCalls' + params);
                },
                getCallRecord: function (params) {
                    return $http.get('/getCallRecord' + params)
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
