var loader = (function () {
    var _container = '.loader-container';
    return {
        show: function () {
            $(_container).fadeIn(200);
        },
        hide: function () {
            $(_container).fadeOut(200)
        }
    }
})();
