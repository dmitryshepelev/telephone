var controller = (function () {
    $(document).ready(function () {
        new Taber('#taber', [
            { name: 'Новые подписки', url: '/admin/getTransacts/pending/', active: true },
            { name: 'Архив', url: '/admin/getTransacts/archive/' },
            { name: 'История', url: '/admin/getTransacts/history/' }
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