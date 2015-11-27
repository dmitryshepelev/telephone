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
        $.get('/services/search?q=' + value, function (result) {
            console.log(result);
            var groups = [];

            var scrb_transacts = result.scrb_transacts;
            if (scrb_transacts.length != 0) {
                var group = $('<div class="search-result-group"><h4 class="search-result-group-header search-result-item">Подписки</h4></div>');
                var content = $('<div class="search-result-content"></div>');
                var itemTemplate = '<div class="search-result-item"><p>{0}</p><span>{1}</span><span class="pull-right">{2}</span></div>';
                scrb_transacts.forEach(function (transact) {
                    content.append(itemTemplate.format(transact.transact_id, transact.username, transact.creation_date))
                });
                group.append(content);
                groups.push(group)
            }

            var pr_transacts = result.pr_transacts;
            if (pr_transacts.length != 0) {
                var group = $('<div class="search-result-group"><h4 class="search-result-group-header search-result-item">Заявки</h4></div>');
                var content = $('<div class="search-result-content"></div>');
                var itemTemplate = '<div class="search-result-item"><p>{0}</p><span>{1}</span><span class="pull-right">{2}</span></div>';
                pr_transacts.forEach(function (transact) {
                    content.append(itemTemplate.format(transact.transact_id, transact.email, transact.creation_date))
                });
                group.append(content);
                groups.push(group)
            }

            var profiles = result.profiles;
            if (profiles.length != 0) {
                var group = $('<div class="search-result-group"><h4 class="search-result-group-header search-result-item">Пользователи</h4></div>');
                var content = $('<div class="search-result-content"></div>');
                var itemTemplate = '<div class="search-result-item"><p>{0}</p><span>{1}</span></div>';
                profiles.forEach(function (profile) {
                    content.append(itemTemplate.format(profile.username, profile.email))
                });
                group.append(content);
                groups.push(group)
            }

            var container = $('<div class="search-result-container" style="display: none"></div>');
            if (groups) {
                groups.forEach(function (group) {
                    container.append(group);
                })
            } else {
            //    no search result
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
            _query.timeouted = true;
            window.setTimeout(function () {
                _query.value = $(e.target).val();
                if (_query.value) {
                    _search(_query.value)
                }
            }, 1000)
        }
    }

    $(document).ready(function () {
        _getProfileInfo(_initProfileContainer());
    });

    return {
        initTooltips: _initTooltips,
        onSearchQueryChange: _onSearchQueryChange
    }
})();