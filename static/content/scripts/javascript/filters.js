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
            return (min > 0 ? min + ' мин ' : '') + (sec < 10 ? '0' + sec : sec) + ' сек';
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

    .filter('callsFilter', ['$filter', function ($filter) {
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
