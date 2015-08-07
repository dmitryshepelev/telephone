(function () {
    angular.module('controllers', ['ngAudio'])

        .controller('ctrl', ['$scope', 'callsFactory', 'ngAudio', '$filter', '$modal', function ($scope, callsFactory, ngAudio, $filter, $modal) {
            var _calls = [];

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
                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: 'get_period_modal_template',
                    controller: 'periodModalCtrl',
                    resolve: {
                        period: function () {
                            return $scope.period;
                        }
                    }
                });

                modalInstance.result.then(function (period) {
                    $scope.period = period;
                    $scope.periodLabeltext = $scope.period.toPeriodString();
                })
            };

            callsFactory.loadCalls().success(function (data) {
                if (data) {
                    _calls = $filter('callsFilter')($filter('callsProxy')(converter.csv_to_json(data)));
                    $scope.calls = _calls;
                } else {
                    throw 'Empty Response';
                }
            });

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
        }])

        .controller('periodModalCtrl', ['$scope', '$modalInstance', 'period', function ($scope, $modalInstance, period) {
            $scope.cancel = function () {
                $modalInstance.dismiss('cancel')
            };

            $scope.ok = function () {
                $modalInstance.close(new Period($scope.dates.from, $scope.dates.to));
            };

            $scope.dates = {
                maxDate: period.getMaxDate(),
                from: period.getFromDate(),
                to: period.getToDate()
            };

            //$scope.getDateDifference = function () {
            //    var timeDiff = Math.abs($scope.dates.to.getTime() - $scope.dates.from.getTime());
            //    return Math.ceil(timeDiff / (1000 * 3600 * 24));
            //}
        }])
})();
