(function (ng) {
    function _config($stateProvider, $urlRouterProvider, $interpolateProvider, $httpProvider, cfpLoadingBarProvider) {
        var _baseUrl = '';

        cfpLoadingBarProvider.includeSpinner = false;
        cfpLoadingBarProvider.includeBar = true;

        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        $urlRouterProvider.when('', '/st');
        $stateProvider
            .state('my', {
                abstract: true,
                url: '',
                templateUrl: _baseUrl + '/uiview/'

            })
            .state('my.st', {
                url: '/st',
                templateUrl: _baseUrl + '/st/',
                controller: 'StCtrl',
                data: {
                    title: 'Статистика'
                }
            })
            .state('my.cst', {
                url: '/cst',
                templateUrl: _baseUrl + '/cst/',
                controller: 'CheckCallCostCtrl',
                data: {
                    title: 'Стоимость звонка'
                }
            })
            .state('my.clb', {
                url: '/clb',
                templateUrl: _baseUrl + '/clb/',
                controller: 'CbCtrl',
                data: {
                    title: 'Обратный звонок'
                }
            })
            .state('my.sf', {
                url: '/sf',
                templateUrl: _baseUrl + '/sf/',
                controller: '',
                data: {
                    title: 'Продление подписки'
                }
            })
            .state('my.blc', {
                url: '/blc',
                templateUrl: _baseUrl + '/blc/',
                controller: '',
                data: {
                    title: 'Пополнение счета'
                }
            })
            .state('my.gscpt', {
                url: '/gscpt',
                templateUrl: _baseUrl + '/gscpt/',
                controller: '',
                data: {
                    title: 'Получить скрипт виджета'
                }
            });
}

    ng.module('mainApp', [
        'ui.router',
        'ui.grid',
        'ui.grid.pagination',
        'ui.grid.autoResize',
        'angular-loading-bar',
        'ngAnimate',
        'ui.bootstrap.position',
        'toastr',
        'ui.bootstrap.debounce',
        'ui.bootstrap.typeahead',
        'uib/template/typeahead/typeahead-popup.html',
        'uib/template/typeahead/typeahead-match.html',
        'ui.bootstrap.tabs',
        'uib/template/tabs/tabset.html',
        'uib/template/tabs/tab.html'
    ]);

    ng.module('mainApp')
        .config(['$stateProvider', '$urlRouterProvider', '$interpolateProvider', '$httpProvider', 'cfpLoadingBarProvider', _config]);


})(angular);