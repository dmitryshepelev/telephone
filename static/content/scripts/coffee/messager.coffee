Messager = (() ->
	Messager = () ->
		@_element = {}
		@_id = 'messager'
		@_template = '<div id="' + this._id + '" align="center" style="display: none"></div>'
		@_initElement()
		return

	Messager.prototype =
		constructor: Messager
		_initElement: () ->
			$('header').prepend @_template;
			@_element = $('#' + @_id)
			@_element.on 'click', @_hide.bind @
			return

		_setValues: (text, type) ->
			@_element.addClass 'message-' + type
			@_element.text text
			return

		_hide: () ->
			@_element.fadeOut 200, () ->
				@_element.removeClass()
				@_element.text ''
				return
			# TODO: .bind @;

		_show: (text, type) ->
			@_setValues text, type
			@_element.fadeIn 200
			return

		success: (text) ->
			@_show text, 'success'
			return

		warning: (text) ->
			@_show text, 'warning'
			return

		error: (text) ->
			@_show text, 'error'
			return

		info: (text) ->
			@_show text, 'info'
			return
)