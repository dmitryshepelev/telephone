(function ($, d) {
    var reqInx = 0;

    function onReady() {
        checkCall(reqInx);
    }

    function checkCall (inx) {
        if (inx < 3) {
            setTimeout(sendRequest, 5000);
        }
        return 0;
    }

    function sendRequest () {
        $.ajax({
            method: 'GET',
            url: 'http://127.0.0.1:8001/chkinc/3e3fd376cff0475b857061c6cd5cecfd/',
            crossDomain: true
        }).done(function (response, text, jqXHR) {
            if (jqXHR.status == 200) {
                // show modal
            } else {
                checkCall(++reqInx);
            }
        }).fail(function() {
            checkCall(++reqInx);
        })
    }

    $(d).ready(onReady);

})($, document);
