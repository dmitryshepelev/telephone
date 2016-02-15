var ctrl = (function ($) {

    return {
        getScript: function () {
            var element = $('input[name="counterNumber"]');
            var value = element.val();

            if (!value) {
                message.error('Заполните поле');
                return 0;
            }

            $.post('/getscript/', {counterNumber: value}, function (result) {
                console.log();
            }).error(function () {
                console.log('error');
            })

        }
    }

})(jQuery);
