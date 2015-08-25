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

    function _makeSortable() {
        $('#callsTable').tablesorter({sortList: [[2,1]], cssAsc: 'table-sort table-sort-asc', cssDesc: 'table-sort table-sort-desc', textExtraction: function (node) {
            var value = node.innerHTML;
            if (value.search(/(мин|сек)/g) != -1) {
                var textArr = value.split(' ');
                value = (textArr.length === 2 ? textArr[0] : Number(textArr[0]) * 60 + Number(textArr[2])).toString();
            }
            return value
        }});
    }

    function _updateContainer(data) {
        var loaderTemplate = '<div align="center"><img src="/static/content/images/loader.gif" class="loader"></div>';
        _container.empty();
        _container.append(data.toString() === 'true' ? loaderTemplate : data);
        _makeSortable();
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

        var elements = $('switcher');
        for (var i = 0; i < elements.length; i++){
            new Switcher(elements[i]);
        }
    });

    return {
        applyFilters: function () {
            var params = _collectData();
            var request_string = new ApiParams(params).getRequestString();
            _getCalls(request_string);
        }
    };
})();