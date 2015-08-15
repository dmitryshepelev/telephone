var audio = (function () {
    var _playClass = 'glyphicon-play';
    var _stopClass = 'glyphicon-stop';
    var _audioElement = document.createElement('audio');
    var _url = '/getCallRecord?id=';

    _audioElement.addEventListener('ended', function () {
        _reset_buttons()
    });

    function _reset_buttons() {
        _update_status.apply($('.' + _stopClass));
    }

    function _update_status() {
        if ($(this).hasClass(_playClass)) {
            $(this).removeClass(_playClass).addClass(_stopClass);
        } else {
            $(this).removeClass(_stopClass).addClass(_playClass);
        }
    }

    function _play(recordId) {
        _audioElement.setAttribute('src', _url + recordId);
        console.log(_audioElement);
        try {
            _audioElement.play()
        } catch (e) {
            // For Chrome
            _audioElement.Play()
        }
    }

    function _stop() {
        try {
            _audioElement.pause()
        } catch (e) {
            _audioElement.Stop()
        }
    }

    return {
        action: function (event) {
            var element = event.target;
            if ($(element.children).hasClass(_playClass)) {
                console.log(element);
                _play(element.attributes['data-record-id'].value);
                _reset_buttons();
            } else {
                _stop()
            }
            _update_status.apply(event.target.children)
        },
        download: function (event) {
            window.location.href = _url + event.target.attributes['data-record-id'].value
        }
    }
})();