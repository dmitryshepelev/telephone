var loader = (function () {
    var _id = 'loader';
    var _template = '<div id="' + _id + '" class="loader-main" align="center"><img src="/static/content/images/loader.gif" /></div>';

    return {
        show: function () {
            $('body').append(_template);
        },
        hide: function () {
            $('body').children('#' + _id).remove()
        }
    }
})();
