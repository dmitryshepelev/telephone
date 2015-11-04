var transact = (function () {
    var _emptyRow = '<tr><td colspan="{0}" align="center">{1}</td></tr>';

    function _getRow (targetNode) {
        return $(targetNode).parents('tr');
    }

    function _deleteRow(row) {
        var tbody = row.parents('tbody');
        var rowNumber = tbody.children().length - 1;
        row.hideElement(200, function () {
            this.remove();
            if (rowNumber == 0) {
                tbody.append(_emptyRow.format(7, 'Нет новых транзакций'));
            }
        });
    }

    function _getTransactId (jqElement) {
        var attrName = 'data-transact-id';
        return $(jqElement).attr(attrName);
    }

    return {
        executeAction: function (e) {
            var target = e.target;
            var row = _getRow(target);
            var transactId = _getTransactId(row);
            var actionId = $(target).attr('data-action-id');
            if (transactId && actionId) {
                $.post('/services/transactAction/', {transactId: transactId, actionId: actionId}, function (data) {
                    if (data.transactId && data.transactId == transactId) {
                        _deleteRow(row)
                    }
                }).fail(function () {

                })
            }
        }
    }
})();
