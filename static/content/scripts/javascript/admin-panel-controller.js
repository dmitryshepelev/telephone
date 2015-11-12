var controller = (function () {
    $(document).ready(function () {
        new Taber('#taber', [
            { name: 'Новые подписки', url: '/admin/getPendingTransacts/' },
            { name: 'Архив', url: '/admin/getArchiveTransacts/' },
            { name: 'История', url: '/admin/getHistoryTransacts/' }
        ], {
            afterChange: function () {
                services.makeSortable('.tablesorter')
            }
        });

        $('#transact-id-search').on('input', function (e) {
            var element = $(e.target);
            var value = element.val();
            filterTable('table').searchRows(value);
        })
    });

    function filterTable (selector) {
        var table = $(selector);
        var colNumber = table.find('th').length;
        var body = table.children('tbody');
        var emptyRow = $('<tr id="emptyRow" style="display: none"><td colspan={0}>Нет совпадений</td></tr>'.format(colNumber));
        return {
            searchRows: function (value) {
                $('#emptyRow').remove();
                var re = new RegExp(value);
                var rows = body.children('tr');
                var rowsFound = 0;
                $.each(rows, function (index, row) {
                    row = $(row);
                    var sourceCells = row.children('td[allow-search]');
                    var targetCells = sourceCells.filter(function (index, cell) {
                        return $(cell).text().match(re);
                    });
                    if (targetCells.length == 0) {
                        row.hideElement();
                    } else {
                        row.showElement();
                        rowsFound++
                    }
                });
                if (rowsFound === 0) {
                    body.append(emptyRow);
                    emptyRow.showElement();
                }
            }
        }
    }
})();