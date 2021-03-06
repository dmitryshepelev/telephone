var audio = (function () {
    var _playClass = 'icon-play';
    var _stopClass = 'icon-stop2';
    var _audioElement = document.createElement('audio');
    _audioElement.setAttribute('type', 'audio/mp3');
    var _url = '/getCallRecord?call_id=';

    _audioElement.addEventListener('ended', function () {
        _reset_buttons()
    });

    function _reset_buttons() {
        _update_status.apply($('.' + _stopClass));
    }

    function _update_status() {
        if ($(this).hasClass(_playClass)) {
            $(this).removeClass(_playClass).addClass(_stopClass);
            $(this).parent().removeClass('btn-default').addClass('btn-danger-wt');
        } else {
            $(this).removeClass(_stopClass).addClass(_playClass);
            $(this).parent().removeClass('btn-danger-wt').addClass('btn-default');
        }
    }

    function _play(recordId) {
        _audioElement.setAttribute('src', _url + recordId);
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

    function _getId(element) {
        var attr = 'data-call-id';
        return $(element).closest('tr[{0}]'.format(attr)).attr(attr);
    }

    return {
        action: function (event) {
            var element = event.target;
            if (event.target.localName == 'span') {
                element = event.target.parentElement;
                event.stopImmediatePropagation()
            }
            if ($(element.children).hasClass(_playClass)) {
                _play(_getId(element));
                _reset_buttons();
            } else {
                _stop()
            }
            _update_status.apply(element.children)
        },
        download: function (event) {
            window.location.href = _url + _getId(event.target)
        }
    }
})();