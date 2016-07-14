(function (ng) {

    function _stCtrl($scope, $apiSrv, toastr, $timeout) {

        $scope.stat = {
            period: {
                start: new Date().toRightDatetimeString(),
                end: new Date().toRightDatetimeString()
            },
            types: [],
            calls: [],
            stat: {}
        };
        
        $scope.statParams = {
            startDate: new Date(),
            endDate: new Date(),
            status: 0,
            types: []
        };
        
        $scope.startDateCalendar = {
            opts: {
                maxDate: $scope.statParams.endDate,
                showWeeks: false
            },
            opened: false,
            open: function () {
                this.opened = true;
            }
        };

        $scope.endDateCalendar = {
            opts: {
                minDate: $scope.statParams.startDate,
                showWeeks: false
            },
            opened: false,
            open: function () {
                this.opened = true;
            }
        };

        $scope.cbPopover = {
            el: document.querySelector('#cb-popover'),
            isShown: false,
            isCalling: false,
            data: {
                price: '',
                number: '',
                description: '',
                prefix: ''
            },
            call: function () {
                var self = this;
                self.isCalling = true;
                var toastTitle = 'Обратный звонок';
                $timeout(function () {
                    $apiSrv.cbCall(self.data.number)
                        .then(function (response) {
                            self.hide();
                            toastr.success('Запрос звонка на номер <strong>' + self.data.number + '</strong> успешно отправлен', toastTitle);
                        })
                        .catch(function () {
                            toastr.error('Операция временно недоступна. Повторите попытку позже', toastTitle);
                        })
                        .then(function () {
                            self.isCalling = false;
                        })
                }, 3000)
            },
            show: function () {
                this.isShown = true;
            },
            hide: function () {
                this.isShown = false;
            },
            toggle: function () {
                this.isShown = !this.isShown;
            }
        };

        $scope.gridOptions = {
            enableHorizontalScrollbar: 0,
            enableVerticalScrollbar: 0,
            enablePaginationControls: false,
            paginationPageSizes: [20],
            paginationPageSize: 20,
            rowHeight: 40,
            data: [],
            columnDefs: [
                { name: 'num', maxWidth: 20, displayName: '', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.renderContainers.body.visibleRowCache.indexOf(row) + 1 ]]</div>' },
                { name: 'date', displayName: 'Дата', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ row.entity.date|date:"dd.MM.yyyy HH:mm:ss":"+0000" ]]</div>' },
                { name: 'type', maxWidth: 20, displayName: '', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents"><span class="[[ grid.appScope.formatType(grid, row) ]]" title="[[ grid.appScope.formatTypeLoclze(grid, row) ]]"></span></div>' },
                { name: 'sip', minWidth: 200, displayName: 'Номер звонящего', enableColumnMenu: false, cellTemplate: '<div popover ng-click="grid.appScope.onSipCellClick($event, row)" class="pointer ui-grid-cell-contents" ng-class="{\'text-bold\': row.entity.is_first_call}">[[ row.entity.caller.sip ]]</div>' },
                { name: 'destination', displayName: 'Номер ответа', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ row.entity.destination || "-" ]]</div>' },
                { name: 'bill_seconds', displayName: 'Время разговора', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.appScope.formatSec(grid, row) ]]</div>' },
                { name: 'rec', maxWidth: 80, minWidth: 80,  displayName: '', enableColumnMenu: false, cellTemplate: '<track-buttons track-id="[[ row.entity.call_id ]]" ng-show="row.entity.status.name == \'answered\'"></track-buttons>' },
                { name: 'cost', displayName: 'Цена минуты', enableColumnMenu: false },
                { name: 'bill_cost', displayName: 'Стоимость', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ grid.appScope.formatCost(grid, row) ]]</div>' },
                { name: 'description', displayName: 'Описание', enableColumnMenu: false, cellTemplate: '<div class="ui-grid-cell-contents">[[ row.entity.caller.description || "-" ]]</div>' }
            ],
            onRegisterApi: function (gridApi) {
                $scope.gridApi2 = gridApi;
            }
        };

        $scope.onSipCellClick = function ($event, row) {
            var el = $($event.target);
            var sip = row.entity.caller.sip;
            $apiSrv.getCallCost(sip)
                .success(function (result) {
                    var callCostInfo = result.data.call_cost_info;
                    $scope.cbPopover.data.price = callCostInfo.price + ' ' + callCostInfo.currency;
                    $scope.cbPopover.data.description = callCostInfo.description;
                    $scope.cbPopover.data.number = sip;
                    $scope.cbPopover.data.prefix = callCostInfo.prefix;

                    if (!$scope.cbPopover.isShown) {
                        $scope.cbPopover.show();
                    }
                })
                .error(function () {
                    console.log(arguments)
                });
        };

        $scope.changeStatType = function (type) {
            var index = $scope.statParams.types.indexOf(type);
            if (index > -1) {
                $scope.statParams.types.splice(index, 1);
            } else {
                $scope.statParams.types.push(type);
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
            var type = row.entity.type.name;
            var disp = row.entity.status.name;

            var icon = 'icon-' + (type === 'incoming' ? 'arrow-down' : (type === 'coming' ? 'arrow-up' : 'loop'));
            var status = 'text-' + (disp === 'answered' ? 'success' : 'error');

            return icon + ' ' + status;
        };

        $scope.formatCost = function (grid, row) {
            var value = row.entity.bill_cost;
            if (!value) return '-';
            return Math.round(value * 100) / 100;
        };

        $scope.formatSec = function(grid, row) {
            var value = row.entity.bill_seconds;
            if (!value) return '-';
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

        $scope.loadStat = function () {
            loadStat()
        };

        function onGetStatSuccess(result) {
            $scope.stat.calls = result.data.calls || [];
            $scope.gridOptions = { data: $scope.stat.calls };
        }

        function onGetStatError() {
            toastr.error('Операция временно недоступна. Повторите попытку позже', 'Статистика звонков');
        }

        function loadStat() {
            var params = {
                start: $scope.statParams.startDate.getTime(),
                end: $scope.statParams.endDate.getTime(),
                status: $scope.statParams.status,
                call_type: $scope.statParams.types.join(' ')
            };
            $apiSrv.getStat(params)
                .success(onGetStatSuccess)
                .error(onGetStatError);
        }

        loadStat();
    }

    _stCtrl.$inject = ['$scope', '$apiSrv', 'toastr', '$timeout'];

    ng.module('mainApp')
        .controller('StCtrl', _stCtrl)

})(angular);