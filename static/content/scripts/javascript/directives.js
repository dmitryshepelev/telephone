angular.module('directives', [])

    .directive('sorting', [function () {
        return {
            restrict: 'A',
            link: function (scope, element, attrs, fn) {
                var defaultClasses = 'glyphicon glyphicon-right glyphicon-sort vis-hidden';
                var iconTemplate = '<span class="' + defaultClasses + '" aria-hidden="true"></span>';
                element.append(iconTemplate);
                element.addClass('pointer');

                if (!scope.order) {
                    scope.order = {
                        parameter: 'time',
                        reverse: true
                    };
                    scope.$apply();
                }

                element.on('click', function (event) {
                    scope.$apply(function () {
                        if (scope.order.parameter != attrs.sorting) {
                            var oldElement = angular.element('th[sorting=' + scope.order.parameter + ']');
                            oldElement.children().removeClass().addClass(defaultClasses);
                        }
                        scope.order.parameter = attrs.sorting;
                        scope.order.reverse = !scope.order.reverse;
                        element.children().removeClass().addClass('glyphicon glyphicon-right glyphicon-' + (scope.order.reverse ? 'menu-down' : 'menu-up'));
                    });

                });
            }
        }
    }]);
