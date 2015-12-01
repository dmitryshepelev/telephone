var mainController = (function () {
    var _query = {
        value: null,
        timeouted: false
    };

    function _initTooltips() {
        $('[tooltip]').tooltip();
    }

    function _initProfileContainer() {
        return $('li.profile-info-wt');
    }

    function _getProfileInfo (container) {
        $.get('/getProfileInfo/', function (data) {
            _updateContainer(container, data)
        })
    }

    function _updateContainer (container, data) {
        container.append(data)
    }

    function _search (value) {
        function _wrapQuery (str, q) {
            var index = str.indexOf(q);
            if (index >= 0) {
                var targetQ = '<strong><u>' + q + '</u></strong>';
                var arr = [str.substr(0, index), targetQ, str.substr(index + q.length)];
                return arr.join('');
            }
            return str;
        }

        $.get('/services/search/?q=' + value, function (result) {
            var groups = [];

            var groupTemplate = '<div class="search-result-group"><h4 class="search-result-group-header">{0}</h4></div>';
            var contentTemplate = '<div class="search-result-content"></div>';
            var itemTemplate = '<div class="search-result-item" data-item-type={0} data-item-id={1} onclick="mainController.toResultItem(event)"><p>{2}</p><span>{3}</span></div>';

            var scrb_transacts = result.scrb_transacts;
            if (scrb_transacts.length != 0) {
                var group = $(groupTemplate.format('Подписки'));
                var content = $(contentTemplate);
                scrb_transacts.forEach(function (transact) {
                    content.append(itemTemplate.format('scrb', transact.transact_id, _wrapQuery(transact.transact_id, value), transact.username))
                });
                group.append(content);
                groups.push(group)
            }

            var pr_transacts = result.pr_transacts;
            if (pr_transacts.length != 0) {
                var group = $(groupTemplate.format('Заявки'));
                var content = $(contentTemplate);
                pr_transacts.forEach(function (transact) {
                    content.append(itemTemplate.format('pr', transact.transact_id, _wrapQuery(transact.transact_id, value), transact.email))
                });
                group.append(content);
                groups.push(group)
            }

            var profiles = result.profiles;
            if (profiles.length != 0) {
                var group = $(groupTemplate.format('Пользователи'));
                var content = $(contentTemplate);
                profiles.forEach(function (profile) {
                    content.append(itemTemplate.format('profile', profile.email, _wrapQuery(profile.username, value), _wrapQuery(profile.email, value)))
                });
                group.append(content);
                groups.push(group)
            }

            var container = $('<div class="search-result-container" style="display: none"></div>');
            if (groups.length != 0) {
                groups.forEach(function (group) {
                    container.append(group);
                })
            } else {
                var group = $(groupTemplate.format('Нет результатов'));
                var content = $(contentTemplate);

                container.append(group.append(content));
            }

            $('.search-form-wt').append(container);
            container.showElement();
        }).fail(function () {

        }).done(function () {
            _query.timeouted = false
        })
    }

    function _onSearchQueryChange (e) {
        var resultContainer = $('.search-result-container');
        if (resultContainer.length != 0) {
            resultContainer.hideElement(200, function () {
                resultContainer.remove();
            })
        }
        if (!_query.timeouted) {
            window.setTimeout(function () {
                _query.value = $(e.target).val();
                if (_query.value) {
                    _search(_query.value);
                    _query.timeouted = true;
                }
            }, 1000)
        }
    }

    function _toResultItem(e) {
        var element = $(e.target).closest('div[data-item-id]');
        var itemId = element.attr('data-item-id');
        var itemType = element.attr('data-item-type');
        window.location.href = '/services/element/{0}/{1}'.format(itemType, itemId);
    }

    function _deleteRow(row) {
        var _emptyRow = '<tr><td colspan="{0}" align="center">{1}</td></tr>';
        var tbody = row.parents('tbody');
        var rowNumber = tbody.children().length - 1;
        row.hideElement(200, function () {
            this.remove();
            if (rowNumber == 0) {
                tbody.append(_emptyRow.format(7, 'Нет новых транзакций'));
            }
        });
    }

    $(document).ready(function () {
        _getProfileInfo(_initProfileContainer());
    });

    return {
        initTooltips: _initTooltips,
        onSearchQueryChange: _onSearchQueryChange,
        toResultItem: _toResultItem,
        deleteRow: _deleteRow
    }
})();