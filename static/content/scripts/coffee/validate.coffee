validate = (() ->
	errorElementCssClass = 'error'
	errorMessageCssClass = 'error-text'

	isElementHasError = (element) ->
		element.hasClass(errorElementCssClass)

	getErrorMessageHTML: (arr) ->
		errorsHTML = ''
		arr.forEach((error) ->
			errorsHTML += '<span class="' + errorMessageCssClass + '">' + error + '</span>'
			return
		)
		return errorsHTML

	showError: (element, errorHTML) ->
		@hideError(element) if isElementHasError(element)
		element.addClass(errorElementCssClass)
		element.after(errorHTML)
		return

	hideError: (element) ->
		if isElementHasError(element)
			element.removeClass(errorElementCssClass)
			nextElement = element.next()
			nextElement.remove() if nextElement.hasClass(errorMessageCssClass)
		return
)()