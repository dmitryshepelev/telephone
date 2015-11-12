var mainController = (function () {
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

    $(document).ready(function () {
        _getProfileInfo(_initProfileContainer());
    });

    return {
        initTooltips: _initTooltips
    }
})();