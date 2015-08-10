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
                        _calls = $filter('callsFilter')($filter('callsProxy')(converter.csv_to_json(data)));
                        $scope.calls = _calls;
                    } else {
                        throw 'Empty Response';
                    }
                }).error(function (e) {
                    window.location.href = '/e/'
                }).finally(function () {
                    $scope.isLoaded = true;
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
                    call.record.audio = ngAudio.load('/getCallRecord?id=' + call.record.id);
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
                        window.location.href = ('/getCallRecord?recordId=' + recordId);
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
