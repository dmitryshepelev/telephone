var transact = (function () {

    function _getRow (targetNode) {
        return $(targetNode).parents('tr');
    }

    function _getTransactId (jqElement) {
        var attrName = 'data-transact-id';
        return $(jqElement).closest('[' + attrName + ']').attr(attrName);
    }

    return {
        executeAction: function (e, onSuccess) {
            e.stopImmediatePropagation();
            var target = e.target;
            var row = _getRow(target);
            var transactId = _getTransactId(target);
            var actionName = $(target).attr('data-action-name');
            if (transactId && actionName) {
                var params = { transactId: transactId };
                if (actionName === 'newuser') {
                    window.location.href = '/admin/' + actionName + '?transact_id=' + params.transactId;
                    return !0;
                }
                $.post('/services/transactAction/{0}/'.format(actionName), params, function (data) {
                    if (data.transactId && data.transactId == transactId) {
                        services.executeCallback(onSuccess, row ? row : undefined)
                    }
                }).fail(function () {
                    message.error('Операция завершена с ошибкой')
                })
            }
        }
    }
})();
