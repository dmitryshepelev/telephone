(function (angular) {

    function _config($stateProvider, $urlRouterProvider, $interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.interceptors.push(function ($q, $ToastrService) {
            function showMessage(message) {
                if (message.text) {
                    $ToastrService[message.type || 'info'](message.text);
                }
            }
            
            function set_detData_attr(response) {
                response.getData = function () {
                    return this.data.data || {};
                }
            }

            return {
                'response': function (response) {
                    if (response.data.message) {
                        showMessage(response.data.message)
                    }
                    set_detData_attr(response);
                    return response || $q.when(response);
                },
                'responseError': function(rejection) {
                    if (rejection.data.message) {
                        showMessage(rejection.data.message)
                    }
                    set_detData_attr(rejection);
                    return $q.reject(rejection);
                }
            }
        });

        $urlRouterProvider.when('', '/login');
        $stateProvider
            .state('auth', {
                abstract: true,
                url: '',
                templateUrl: '/auth/uiview/'
            })
            .state('auth.login', {
                url: '/login',
                templateUrl: '/auth/login/',
                controller: '$LoginCtrl',
                data: {
                    title: 'Вход'
                }
            });
    }
    
    angular
        .module('$AuthApp', [
            'ui.router',
            '$validator',
            '$toastr'
        ]);

    angular
        .module('$AuthApp')
            .config(['$stateProvider', '$urlRouterProvider', '$interpolateProvider', '$httpProvider', _config]);

})(angular);