var mainApp = angular.module('mainApp', ['ui.bootstrap', 'ngAudio', 'filters']);


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


mainApp.controller('ctrl', ['$scope', 'callsFactory', 'ngAudio', function ($scope, callsFactory, ngAudio) {
    $scope.calls = [];

    function callsFilter(calls) {
        return calls.filter(function (call) {
            return call['Тип'] != 'внутренний';
        });
    }

    callsFactory.loadCalls().success(function (data) {
        if (data) {
            $scope.calls = callsFilter(converter.csv_to_json(data));
        } else {
            throw 'Empty Response';
        }
    });

    $scope.playingRecord = {};
    $scope.record = function (recordId) {
        function getCallByRecordId (id) {
            return $scope.calls.filter(function (element) {
                return element.record.id == recordId;
            })[0];
        };

        // Select call object which record will be playing
        var call = getCallByRecordId(recordId);

        // creates a copy of current playing record object
        var currentRecord = {};
        for (var prop in $scope.playingRecord) {
            if ($scope.playingRecord.hasOwnProperty(prop)) {
                currentRecord[prop] = $scope.playingRecord[prop];
            }
        }

        if (!currentRecord || currentRecord.id != call.record.id) {
            if (!call.record.audio) {
                // New audio will be played
                // TODO: get record request to the api
                call.record.audio = ngAudio.load('/testrecord?recordId=' + call.record.id);
            };
        }

        return {
            play: function () {
                $scope.playingRecord = call.record.audio;
                $scope.playingRecord.setProgress(call.record.audio.progress || 0);
                $scope.playingRecord.play();
                $scope.playingRecord.playing = call.record.playing = true;
                $scope.playingRecord.id = call.record.id;
            },
            pause: function () {
                $scope.playingRecord.pause();
                $scope.playingRecord.playing = call.record.playing = false;
                call.record.audio = $scope.playingRecord;
            }
        }
    }
}]);