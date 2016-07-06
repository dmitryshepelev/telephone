(function (angular) {

    angular
        .module('$AudioManager', ['ngAudio']);

    angular
        .module('$AudioManager')
        .service('$trackManager', _$trackManager)
        .directive('trackButtons', _$trackButtons);

    _$trackButtons.$inject = ['$apiSrv', '$window', '$trackManager'];
    function _$trackButtons($apiSrv, $window, $trackManager) {
        return {
            restrict: 'E',
            scope: {
                trackId: '='
            },
            template:
                '<button class="btn-xs-wt btn btn-default margin-tb-10 margin-r-5" ng-click="action()"><span ng-class="{\'icon-play\': paused, \'icon-stop2\': !paused}"></span></button>' +
                '<button class="btn-xs-wt btn btn-default margin-tb-10" ng-click="download()"><span class="icon-download"></span></button>',
            controller: function ($scope, $element, $attrs) {
                var src = $apiSrv.downloadCRUrl + $scope.trackId;
                $scope.paused = true;

                $scope.action = function () {
                    if ($trackManager.isTrack()) {
                        if (!$scope.paused) {
                            $scope.paused = true;
                            $trackManager.stop();
                            return;
                        }
                    }
                    $trackManager.setTrack(src);
                    $scope.paused = false;
                    $trackManager.play();
                };
                
                $scope.download = function () {
                    $window.location.href = src;
                }
            }
        }
    }

    _$trackManager.$inject = ['ngAudio'];
    function _$trackManager(ngAudio) {
        var _track = null;
        var _trackId = null;
        var _paused = true;
        
        return {
            setTrack: function (src) {
                if (_track) {
                    _track.stop();
                }
                _track = ngAudio.load(src);
                _trackId = src;
                return _track;
            },
            paused: _paused,
            isTrack: function () {
                return !!_track
            },
            stop: function () {
                _track.stop();
                _paused = true;
            },
            play: function () {
                _track.play();
                _paused = false;
            }
        }
    }

})(angular);
