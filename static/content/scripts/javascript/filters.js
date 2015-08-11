(function () {
    angular.module('filters', [])

        .filter('capitalize', [function () {
            return function (value) {
                return value[0].toUpperCase() + value.slice(1);
            }
        }])

        .filter('fromSeconds', [function () {
            return function(value) {
                var min = Math.floor(value / 60);
                var sec = value - min * 60;
                return (min > 0 ? min + ' мин ' : '') + sec + ' сек';
            }
        }])

        .filter('status', [function () {
            return function (value) {
                return value === 'отвечен';
            }
        }])

        .filter('callTime', [function () {
            return function (value) {
                var dateTime = value.split(' ');
                dateTime[0] = dateTime[0].split('.').reverse().join('-');
                return new Date(dateTime.join('T') + 'Z');
            }
        }])

        .filter('callsProxy', ['$filter', function ($filter) {
            return function (arr) {
                angular.forEach(arr, function (element, index) {
                    if (element.hasOwnProperty('Тип')) {
                        arr[index] = {
                            incoming: $filter('callType')(element['Тип'], false),
                            status: $filter('status')(element['Статус']),
                            time: $filter('callTime')(element['Время']),
                            from: element['Откуда'],
                            responder: element['Кто ответил'],
                            callTime: Number(element['Продолжительность звонка']),
                            talkTime: Number(element['Продолжительность разговора']),
                            record: {
                                id: element['ID записи'],
                                audio: null
                            }
                        };
                    }
                });
                return arr;
            }
        }])

        .filter('callsFilter', [function () {
            return function (calls, filterParams) {
                function _checkParams (call, params) {
                    var isThatCall = true;
                    for (var param in params) {
                        if (params.hasOwnProperty(param) && params[param] != null && call[param] != params[param]) {
                            isThatCall = false;
                            break;
                        }
                    }
                    return isThatCall;
                }
                return calls.filter(function (call) {
                    return call.incoming != undefined && _checkParams(call, filterParams);
                });
            }
        }])

        .filter('callType', [function () {
            return function (value, toString) {
                if (toString) {
                    return value ? 'Входящий' : 'Исходящий';
                } else {
                    return value === 'входящий' ? true : (value === 'исходящий' ? false : undefined);
                }
            }
        }]);
})();
