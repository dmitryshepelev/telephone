audio = (() ->
	_playClass = 'glyphicon-play'
	_stopClass = 'glyphicon-stop'
	_audioElement = document.createElement 'audio'
	_url = '/getCallrecord?id='

	_audioElement.addEventListener 'ended', () -> _reset_buttons()

	_reset_buttons = () ->
		_update_status.apply $ '.' + _stopClass

	_update_status = () ->
		if $(@).hasClass(_playClass) then $(@).removeClass(_playClass).addClass(_stopClass) else $(@).removeClass(_stopClass).addClass(_playClass)

	_play = (recordId) ->
		_audioElement.setAttribute 'src', _url + recordId
		try	_audioElement.play()
		catch e
			_audioElement.Play()
		return

	_stop = () ->
		try	_audioElement.pause()
		catch e
			_audioElement.Stop()
		return

	action: (e) ->
		element = e.target
		if ($(element.children).hasClass _playClass)
			_play element.attributes['data-record-id'].value
			_reset_buttons()
		else
			_stop()
		_update_status.apply element.children
		return
	download: (e) ->
		window.location.href = _url + event.target.attributes['data-record-id'].value
)()