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