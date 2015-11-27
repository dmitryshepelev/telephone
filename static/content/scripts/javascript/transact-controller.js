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
            var actionName = $(target).attr('data-action-name');
            if (transactId && actionName) {
                var params = { transactId: transactId };
                if (actionName === 'newuser') {
                    window.location.href = '/admin/' + actionName + '?transact_id=' + params.transactId;
                    return !0;
                }
                $.post('/services/transactAction/{0}/'.format(actionName), params, function (data) {
                    if (data.transactId && data.transactId == transactId) {
                        _deleteRow(row)
                    }
                }).fail(function () {
                    message.error('Операция завершена с ошибкой')
                })
            }
        }
    }
})();
