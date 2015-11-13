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
            services.filterTable('table').searchRows(value);
        })
    });
})();