var controller = (function () {
    $(document).ready(function () {
        new Taber('#taber-subscribe-transact', [
            { name: 'Новые подписки', url: '/admin/getTransacts/pending/', active: true },
            { name: 'Архив', url: '/admin/getTransacts/archive/' },
            { name: 'История', url: '/admin/getTransacts/history/' }
        ], {
            afterChange: function () {
                services.makeSortable('.tablesorter')
            },
            minContentHeight: 265
        });

        new Taber('#taber-pr-transact', [
            { name: 'Новые заявки', url: '/admin/getPRTransacts/pending/', active: true },
            { name: 'История', url: '/admin/getPRTransacts/history/' }
        ], {
            afterChange: function () {
                services.makeSortable('#pr-transacts')
            },
            minContentHeight: 265
        });
    });

    return {
        showDetails: function (e, type) {
            var transactId = $(e.target).closest('[data-transact-id]').attr('data-transact-id');
            $.get('/services/element/' + type + '/' + transactId + '/?as_partial=True', function (result) {
                $('#element-details').empty().append(result)
            })
        }
    }
})();