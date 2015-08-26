var validate = (function () {
    var errorElementCssClass = 'error';
    var errorMessageCssClass = 'error-text';

    function isElementHasError (element) {
        return element.hasClass(errorElementCssClass);
    }

    return {
        getErrorMessageHTML: function (arr) {
            var errorsHTML = '';
            arr.forEach(function(error) {
                errorsHTML += '<span class="' + errorMessageCssClass + '">' + error + '</span>';
            });
            return errorsHTML;
        },
        showError: function (element, errorHTML) {
            if (isElementHasError(element)) {
                this.hideError(element)
            }
            element.addClass(errorElementCssClass);
            element.after(errorHTML);
        },
        hideError: function (element) {
            if (isElementHasError(element)) {
                element.removeClass(errorElementCssClass);
                var nextElement = element.next();
                if (nextElement.hasClass(errorMessageCssClass)) {
                    nextElement.remove();
                }
            }
        }
    }
})();
