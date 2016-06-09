(function (angular) {
    
    function _LoginCtrl($scope, $ValidateSvc, $http, $location, $ToastrService, $state) {
        
        $scope.loginModel = {};

        function onError(error) {
            if (error instanceof Error) {
                $ToastrService.error();
            }
        }

        $scope.login = function () {
            var validationResult = $ValidateSvc.validateForm($scope.$loginForm);

            if (validationResult.status) {
                $http.post('/auth/api/login/', $scope.loginModel)
                    .then(function (response) {
                        var data = response.getData();
                        window.location.href = data.redirect_url;
                    })
                    .catch(onError)
            }
        };

        $scope.profileRequestModel = {};

        $scope.sendProfileRequest = function () {
            var validationResult = $ValidateSvc.validateForm($scope.$profileRequestForm);

            if (validationResult.status) {
                $http.post('/auth/api/profile_request/', $scope.profileRequestModel)
                    .then(function (response) {
                        var data = response.getData();
                        window.localStorage.setItem('createdTransactionRequest', JSON.stringify(data));
                        $scope.createdProfileRequest = {
                            transact_id: data.transact_id,
                            email: data.email
                        };
                    })
                    .catch(onError)
            }
        };

        $scope.createdProfileRequest = JSON.parse(window.localStorage.getItem('createdTransactionRequest')) || null;

    }
    
    _LoginCtrl.$inject = ['$scope', '$ValidateSvc', '$http', '$location', '$ToastrService', '$state'];

    angular
        .module('$AuthApp')
            .controller('$LoginCtrl', _LoginCtrl)
    
})(angular);
