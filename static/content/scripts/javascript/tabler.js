var tabler = (function () {
    function _getLoadUrl (jqEventTarget) {
        var attrName = 'data-load-content-url';
        return jqEventTarget.parents('table[' + attrName +  ']').attr(attrName)
    }

    return {
        loadPage: function (event, pageNumber) {
            var element = $(event.target);
            var url = _getLoadUrl(element);
            $.get(url + '?page=' + pageNumber, function (result) {
                var tableContainer = element.parents('table').parent();
                tableContainer.hideElement(200, function () {
                    tableContainer.empty();
                    tableContainer.append(result);
                    tableContainer.showElement()
                })
            }).fail(function () {
                message.error('Произошла ошибка при загрузке данных')
            })
        }
    }
})();
