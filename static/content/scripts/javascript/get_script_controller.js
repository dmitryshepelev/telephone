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
                $('#code').empty().append(result);
            }).error(function () {
                message.error('Произошла ошибка');
            })

        }
    }

})(jQuery);
