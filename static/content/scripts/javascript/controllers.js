(function () {
    angular.module('controllers', ['ngAudio'])

        .controller('ctrl', ['$scope', 'callsFactory', 'ngAudio', '$filter', '$modal', 'modalsProvider', function ($scope, callsFactory, ngAudio, $filter, $modal, modalsProvider) {
            var _calls = [];
            var _params = new ApiParams();
            var _user = angular.element('input[id=user_code]').val();
            var _tree = angular.element('input[id=schema_code]').val();
            if (!_user || !_tree) {
                window.location.href = '/e/schema/';
            }
            _params.setParams({ user: _user, tree: _tree });
            var _loadCalls = function () {
                $scope.isLoaded = false;
                callsFactory.loadCalls(_params.getRequestString()).success(function (data) {
                    if (data) {
                        _calls = $filter('callsProxy')(converter.csv_to_json(data));
                        $scope.filters.applyFilters();
                    } else {
                        throw 'Empty Response';
                    }
                }).error(function (e) {
                    window.location.href = '/e/'
                }).finally(function () {
                    $scope.isLoaded = true;
                    console.log($scope);
                });
            };

            $scope.isLoaded = false;
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
                changeIncomingFilter: function (value) {
                    $scope.filters.params.incoming = value;
                },
                applyFilters: function () {
                    $scope.calls = $filter('callsFilter')(_calls, $scope.filters.params)
                }
            };

            $scope.period = new Period();
            $scope.periodLabeltext = $scope.period.toPeriodString();
            $scope.showPeriodModal = function () {
                modalsProvider.periodModal({ period: $scope.period }, function (period) {
                    $scope.period = period;
                    $scope.periodLabeltext = $scope.period.toPeriodString();
                    _params.setParams({ from: period._from, to: period._to });
                    _loadCalls();
                });
            };

            $scope.record = function (call) {
                var requestString = '/getCallRecord?id=' + call.record.id;
                // Load new audio
                if (!call.record.audio) {
                    // New audio will be played
                    call.record.audio = ngAudio.load(requestString);
                }

                return {
                    play: function () {
                        console.log(call.record.audio);
                        call.record.audio.play();
                    },
                    stop: function () {
                        call.record.audio.stop();
                    },
                    getCallRecordRequestString: function () {
                        return requestString;
                    }
                }
            };
            _loadCalls();
        }])

        .controller('periodModalCtrl', ['$scope', '$modalInstance', 'period', function ($scope, $modalInstance, period) {
            $scope.dates = {
                maxDate: period.getMaxDate(),
                from: period.getFromDate(),
                to: period.getToDate()
            };

            $scope.errors = [];

            $scope.cancel = function () {
                $modalInstance.dismiss('cancel')
            };

            $scope.ok = function () {
                var period = new Period($scope.dates.from, $scope.dates.to);
                if (period.getDatesDifferent() < 0) {
                    period.setToDate(period.getFromDate());
                }
                $modalInstance.close(period);
            };
        }])
})();
