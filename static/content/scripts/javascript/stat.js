var stat = (function () {
    $(document).ready(function (){
        $.get('/test/', function (result) {
            console.log(result);
            var jsonStr = conventer.csv_to_json(result);
            console.log(jsonStr)
        })
    })
})();