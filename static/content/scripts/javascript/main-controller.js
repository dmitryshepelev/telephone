var mainController = (function () {
    function _initTooltips() {
        $('[tooltip]').tooltip();
    }

    function _getProfileInfo () {
        var container = $('li.profile-info-wt');
        $.get('/getProfileInfo/', function (data) {
            _updateContainer(container, data)
        })
    }

    function _updateContainer (container, data) {
        container.append(data)
    }

    $(document).ready(function () {
        _getProfileInfo();
    });

    return {
        initTooltips: _initTooltips
    }
})();