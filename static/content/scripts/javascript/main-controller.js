var mainController = (function () {
    function _initTooltips() {
        $('[tooltip]').tooltip();
    }

    function _initRequiredFields() {
        var template = '<abbr class="required-label-flag" title="Обязательно к заполнению">*</abbr>';
        $('[required]').prev('label[for]').append(template);
    }

    return {
        initTooltips: _initTooltips,
        initRequiredFields: _initRequiredFields
    }
})();

/* APP INIT. GLOBAL VARIABLES */