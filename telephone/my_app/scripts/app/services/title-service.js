(function (ng) {

    function _titleSrv() {
        var title = null;
        return {
            setTitle: function (value) {
                title = value;
            },
            getTitle: function () {
                return title;
            }
        }
    }

    _titleSrv.$inject = [];

    ng.module('mainApp')
        .factory('$titleSrv', _titleSrv)

})(angular);