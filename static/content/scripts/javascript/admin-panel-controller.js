var controller = (function () {
    function _getPendingTransacts() {
        var container = $('#pending-transacts-container');
        $.get('/admin/getPendingTransacts/', function (data) {
            _updateContainer(container, data);
            container.children('table').tablesorter({ cssAsc: 'table-sort table-sort-asc', cssDesc: 'table-sort table-sort-desc' })
        }).fail(function () {
            _updateContainer(container, 'Произошла ошибка при получении данных');
        })
    }

    function _updateContainer (container, data) {
        container.empty().append(data)
    }

    $(document).ready(function () {
        _getPendingTransacts()
    });
})();