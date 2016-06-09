(function (angular) {

    function ToastrService(toastr, $translate) {

        var defaultText = {
            header: {
                success: 'Информация',
                error: 'Ошибка',
                warning: 'Внимание',
                info: 'Информация'
            },
            text: {
                success: 'Операция завершена успешно',
                error: 'Произошла ошибка',
                warning: 'Проверьте правильность данных',
                info: 'Здесь может быть ваша реклама'
            }
        };

        /**
         * Show toast depends on type
         * @param type success error warning info
         * @param text
         * @param header
         */
        function showToast (type, text, header) {
            text = text || defaultText.text[type];
            header = header || defaultText.header[type];

            toastr[type](text, header);
        }

        return {
            /**
             * Show success toast
             * @param text
             * @param header
             */
            success: function (text, header) {
                showToast('success', text, header);
            },
            /**
             * Show error toast
             * @param header
             * @param text
             */
            error: function (text, header) {
                showToast('error', text, header);
            },
            /**
             * Show warning toast
             * @param header
             * @param text
             */
            warning: function (text, header) {
                showToast('warning', text, header);
            },
            /**
             * Show info toast
             * @param header
             * @param text
             */
            info: function (text, header) {
                showToast('info', text, header);
            }
        }
    }

    ToastrService.$inject = ['toastr'];

    angular
        .module('$toastr', ['toastr']);

    function _config(toastrConfig) {
        angular.extend(toastrConfig, {
            maxOpened: 3,
            timeOut: 10000,
            allowHtml: true
        });
    }

    angular
        .module('$toastr')
        .config(['toastrConfig', _config]);
    
    angular
        .module('$toastr')
            .service('$ToastrService', ToastrService);

})(angular);

