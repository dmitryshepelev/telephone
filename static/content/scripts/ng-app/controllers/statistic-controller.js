(function (ng) {

    function _stCtrl($scope, $apiSrv, uiGridConstants) {

        $scope.stat = {
            calls: [],
            stat: {}
        };
        $scope.gridOptions = {
            enableHorizontalScrollbar: 0,
            enableVerticalScrollbar: 0,
            enablePaginationControls: false,
            paginationPageSizes: [20],
            paginationPageSize: 20,
            rowHeight: 40,
            columnDefs: [
                { name: 'num', maxWidth: 20, displayName: '', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.renderContainers.body.visibleRowCache.indexOf(row) + 1 ]]</div>' },
                { name: 'date', displayName: 'Дата', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ row.entity.date|date:"dd.MM.yyyy HH:mm:ss":"+0000" ]]</div>' },
                { name: 'call_type', maxWidth: 20, displayName: '', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents"><span class="[[ grid.appScope.formatType(grid, row) ]]" title="[[ grid.appScope.formatTypeLoclze(grid, row) ]]"></span></div>' },
                { name: 'sip', minWidth: 200, displayName: 'Номер звонящего', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents" ng-class="{\'text-bold\': row.entity.is_first_call}">[[ row.entity.sip ]]</div>' },
                { name: 'destination', displayName: 'Номер ответа', enableColumnMenu: false },
                { name: 'bill_seconds', displayName: 'Время разговора', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.appScope.formatSec(grid, row) ]]</div>' },
                { name: 'rec', maxWidth: 80, minWidth: 80,  displayName: '', enableColumnMenu: false, cellTemplate: '<div>' +
		                    '<button class="btn-xs-wt btn btn-default margin-tb-10 margin-r-5" onclick="audio.action(event)"><span onclick="audio.action(event)" class="icon-play"></span></button>' +
		                    '<button class="btn-xs-wt btn btn-default margin-tb-10" onclick="audio.download(event)"><span class="icon-download"></span></button>' +
		                '</div>' },
                { name: 'cost', displayName: 'Цена минуты', enableColumnMenu: false },
                { name: 'bill_cost', displayName: 'Стоимость', enableColumnMenu: false },
                { name: 'description', displayName: 'Описание', enableColumnMenu: false }
            ],
            onRegisterApi: function (gridApi) {
                $scope.gridApi2 = gridApi;
            }
        };

        $scope.getPagesArr = function (totalPages) {
            return new Array(totalPages);
        };

        $scope.formatTypeLoclze = function (grid, row) {
            var disp = row.entity.disposition;
            switch (disp) {
                case 'answered':
                    return 'Отвечен';
                case 'busy':
                    return 'Занято';
                case 'cancel':
                    return 'Отменен';
                case 'no answer':
                    return 'Нет ответа';
                case 'failed':
                    return 'Неудачный';
                case 'no money':
                    return 'Нет средств';
                case 'unallocated number':
                    return 'Номара не существует';
                case 'no limit':
                    return 'Превышен лимит';
                case 'no day limit':
                    return 'Превышен дневной лимит';
                case 'line limit':
                    return 'Превышен лимит линии';
                default:
                    return '';
            }
        };

        $scope.formatType = function (grid, row) {
            var type = row.entity.call_type;
            var disp = row.entity.disposition;

            var icon = 'icon-' + (type === 'incoming' ? 'arrow-down' : (type === 'coming' ? 'arrow-up' : 'loop'));
            var status = 'text-' + (disp === 'answered' ? 'success' : 'error');

            return icon + ' ' + status;
        };

        $scope.formatSec = function(grid, row) {
            var value = row.entity.bill_seconds;
            var min = Math.floor(value / 60);
            var sec = value - min * 60;
            return (min > 0 ? min + ' мин ' : '') + (sec + ' сек');
        };

        $scope.getTableHeight = function() {
            var rowHeight = 40; // your row height
            var headerHeight = 40; // your header height
            return {
                height: ($scope.gridOptions.data.length * rowHeight + headerHeight) + "px"
            };
        };

        function onGetStatSuccess(response) {
            $scope.stat.calls = response.calls || [];
            $scope.gridOptions = { data: $scope.stat.calls };
        }

        function onGetStatError() {

        }

        $apiSrv.getStat()
            .success(onGetStatSuccess)
            .error(onGetStatError)

    }

    _stCtrl.$inject = ['$scope', '$apiSrv', 'uiGridConstants'];

    ng.module('mainApp')
        .controller('StCtrl', _stCtrl)

})(angular);
