var mainApp = angular.module('mainApp', ['ui.bootstrap', 'ngAudio']);


mainApp.filter('capitalize', [function () {
    return function (value) {
        return value[0].toUpperCase() + value.slice(1);
    }
}]);


mainApp.filter('fromSeconds', [function () {
    return function(value) {
        var min = Math.floor(value / 60);
        var sec = value - min * 60;
        return (min > 0 ? min + ' мин ' : '') + (sec < 10 ? '0' + sec : sec) + ' сек';
    }
}]);


mainApp.filter('status', [function () {
    return function (value) {
        return value === 'отвечен';
    }
}]);


mainApp.filter('callTime', [function () {
    return function (value) {
        var dateTime = value.split(' ');
        dateTime[0] = dateTime[0].split('.').reverse().join('-');
        return new Date(dateTime.join('T') + 'Z');
    }
}]);

mainApp.filter('callsFilter', ['$filter', function ($filter) {
    return function (arr) {
        angular.forEach(arr, function (element, index) {
            if (element.hasOwnProperty('Тип')) {
                arr[index] = {
                    type: element['Тип'],
                    status: $filter('status')(element['Статус']),
                    time: $filter('callTime')(element['Время']),
                    from: element['Откуда'],
                    responder: element['Кто ответил'],
                    callTime: element['Продолжительность звонка'],
                    talkTime: element['Продолжительность разговора'],
                    record: {
                        id: element['ID записи'],
                        playing: false,
                        audio: null
                    }
                };
            }
        });
        return arr;
    }
}]);


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
        var call = $scope.calls.filter(function (element) {
            return element.record.id == recordId;
        })[0];

        if (!$scope.currentRecord || $scope.currentRecord.id !=  recordId) {
            if (!call.record.audio) {
                // TODO: get record request to the api
                $scope.currentRecord = ngAudio.load('/testrecord?recordId=' + recordId);
                call.record.audio = $scope.currentRecord;
            } else {
                $scope.currentRecord = call.record.audio;
            }
            $scope.currentRecord.id = recordId;
        }
        console.log($scope.calls);
        return {
            play: function () {
                $scope.currentRecord.setProgress(call.record.audio.progress);
                $scope.currentRecord.play();
                $scope.currentRecord.playing = call.record.playing = true;
            },
            pause: function () {
                $scope.currentRecord.pause();
                $scope.currentRecord.playing = call.record.playing = false;
                call.record.audio = $scope.currentRecord;
            }
        }

    }
}]);