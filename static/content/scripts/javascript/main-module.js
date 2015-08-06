var mainApp = angular.module('mainApp', ['ui.bootstrap', 'ngAudio', 'filters', 'directives', 'nzToggle']);


mainApp.factory('callsFactory', ['$http' ,function ($http) {
    var testMode = true;
    // TODO: url to the api
    var baseUrl = testMode ? '/test/' : '';
    // TODO: params array to request request
    return {
        loadCalls: function () {
            return $http.get(baseUrl);
        }
    }
}]);


mainApp.controller('ctrl', ['$scope', 'callsFactory', 'ngAudio', '$filter', function ($scope, callsFactory, ngAudio, $filter) {
    var _calls = [];

    $scope.calls = [];
    $scope.order = {
        parameter: 'time',
        reverse: true
    };

    $scope.filters = {
        params: {
            incoming: null,
            status: null
        },
        onIncomingFilterChange: function () {
            $scope.calls = $filter('callsFilter')(_calls, $scope.filters.params);
        },
        onStatusFilterChange: function () {
            $scope.calls = $filter('callsFilter')(_calls, $scope.filters.params);
        },
        changeIncomingFilter: function (value) {
            $scope.filters.params.incoming = value;
        },
        changeStatusFilter: function (value) {
            $scope.filters.params.status = value;
        }
    };

    callsFactory.loadCalls().success(function (data) {
        if (data) {
            _calls = $filter('callsFilter')($filter('callsProxy')(converter.csv_to_json(data)));
            $scope.calls = _calls;
        } else {
            throw 'Empty Response';
        }
    });

    $scope.record = function (recordId) {
        function getCallByRecordId (id) {
            return $scope.calls.filter(function (element) {
                return element.record.id == recordId;
            })[0];
        }

        var call = getCallByRecordId(recordId);

        // Load new audio
        if (!call.record.audio) {
            // New audio will be played
            // TODO: get record request to the api
            call.record.audio = ngAudio.load('/testrecord?recordId=' + call.record.id);
        }

        return {
            play: function () {
                call.record.audio.setProgress(call.record.audio.progress || 0);
                call.record.audio.play();
                call.record.playing = true;
            },
            pause: function () {
                call.record.audio.pause();
                call.record.playing = false;
            },
            getRecord: function () {
                window.location.href = ('/testrecord?recordId=' + recordId);
            }
        }
    }
}]);