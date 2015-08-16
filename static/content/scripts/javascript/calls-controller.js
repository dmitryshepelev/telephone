var controller = (function () {
    var _container = {};

    function _setContainer() {
        _container = $('div[data-view]');
    }

    function _initDatepicker() {
        var container = $('#datepicker');
        container.datepicker({
            endDate: Date.getNowDate().toRightDateString(),
            todayBtn: 'linked',
            language: 'ru',
            keyboardNavigation: false,
            todayHighlight: true,
            autoclose: true
        }).on('changeDate', function (event) {
            $(event.target).attr('value', event.date.toRightDateString());
        });
        container.find('input.pseudo-hidden').attr('value', Date.getNowDate().toRightDateString());
    }

    function _updateContainer(data) {
        var loaderTemplate = '<div align="center"><img src="/static/content/images/loader.gif" class="loader"></div>';
        _container.empty();
        _container.append(data.toString() === 'true' ? loaderTemplate : data);
    }

    function _getCalls(request_string, callback) {
        _updateContainer(true);
        $.get('/getCalls/{0}'.format(request_string || ''), function (data) {
            _updateContainer(data);
        }).fail(function () {
            window.location.href = '/e/';
        })
    }

    function _collectData() {
        var data = {};
        var elements = $('input.pseudo-hidden');
        for (var i = 0; i < elements.length; i++) {
            var key = $(elements[i]).attr('name');
            var value = $(elements[i]).attr('value');
            data[key] = Number(value).toString() == 'NaN' ? value : value == 0 ? 2 : value - 1;
        }
        return data;
    }

    $(document).ready(function () {
        _setContainer();
        _initDatepicker();
        _getCalls(new ApiParams().getRequestString());

    });

    return {
        applyFilters: function () {
            var params = _collectData();
            var request_string = new ApiParams(params).getRequestString();
            _getCalls(request_string);
        }
    };
})();