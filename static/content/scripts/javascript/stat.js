var stat = (function () {
    var testMode = true;

    function get_calls_list(params, successCallback, testMode) {
        // TODO: url to the api
        var baseUrl = testMode ? '/test/' : '';
        // TODO: params array to request request
        $.get(baseUrl, function (result) {
            if (result) {
                var calls = converter.csv_to_json(result);
                successCallback.call(this, calls);
            } else {
                throw 'Empty response';
            }
        })
    }

    function showCalls (calls) {
        console.log(calls);
        var container = $('#calls');
        if (calls.length === 0) {
            // TODO: if no calls was found
        } else {
            //var tableIds = table.generateTable(container);
            //table.generateHeader(calls[0], []);
            table.fillTable(calls, []);

        }

    }

    $(document).ready(function (){
        get_calls_list([], showCalls, testMode);
    })
})();