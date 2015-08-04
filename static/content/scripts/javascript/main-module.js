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
    $scope.currentRecord = {};

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

    $scope.record = function (recordId) {
        // Select call object
        var call = $scope.calls.filter(function (element) {
            return element.record.id == recordId;
        })[0];

        // creates a copy of current playing record object
        var playingRecord = {};
        angular.copy($scope.currentRecord, playingRecord);


        if (!$scope.currentRecord || $scope.currentRecord.id !=  recordId) {
            if (!call.record.audio) {
                // New audio will be played
                // TODO: get record request to the api
                call.record.audio = ngAudio.load('/testrecord?recordId=' + recordId);
            } else {
                $scope.currentRecord = call.record.audio;
            }
            $scope.currentRecord.id = recordId;
        }

        return {
            play: function () {
                if ($scope.currentRecord.playing) {
                    console.log(true);
                }
                $scope.currentRecord.setProgress(call.record.audio.progress);
                $scope.currentRecord.play();
                $scope.currentRecord.playing = call.record.playing = true;
            },
            pause: function () {
                if (call.record.playing) {
                    console.log(true);
                }
                $scope.currentRecord.pause();
                $scope.currentRecord.playing = call.record.playing = false;
                call.record.audio = $scope.currentRecord;
            }
        }

    }
}]);