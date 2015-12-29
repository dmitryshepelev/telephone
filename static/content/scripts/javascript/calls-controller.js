var controller = (function () {
    var _container = {};

    function _setContainer() {
        _container = $('div[data-view]');
    }

    function _initDatepicker() {
        var container = $('#datepicker');
        container.datepicker({
            endDate: Date.getNowDate().toRightDatetimeString(),
            todayBtn: 'linked',
            language: 'ru',
            keyboardNavigation: false,
            todayHighlight: true,
            autoclose: true
        }).on('changeDate', function (event) {
            $(event.target).attr('value', event.date.toRightDatetimeString());
        });
        container.find('input.pseudo-hidden').attr('value', Date.getNowDate().toRightDatetimeString());
    }

    function _updateContainer(data) {
        if (data){
            _container.append(data);
            services.makeSortable('#callsTable', [[1,1]]);
            mainController.initTooltips();
            _container.showElement();
            _initPopovers()
        } else {
          _container.hideElement(200, function () {
                _container.empty();
            });
        }
    }

    function _initPopovers() {
        var elements = $('[popover]');
        for (var i = 0; i < elements.length; i++){
            var el = $(elements[i]);
            var number = el.text();
            number = number[0] === '+' ? number.slice(1) : number;
            el.webuiPopover({
                cache: false,
                width: 185,
                animation: 'pop',
                placement: 'right',
                content: function (data) {
                    return '<div style="margin-bottom: 10px;">Стоимость: <strong>' + data.price.toFixed(2) + ' ' + data.currency +'</strong></div>' +
                        '<button class="btn btn-sm-wt btn-default" type="button" style="width: 100%">Позвонить</button>' +
                        '<input type="hidden" value="' + data.phone + '" />';
                },
                type: 'async',
                url: '/getCallCost/?n=' + number
            })
                .on('shown.webui.popover', function (e, target) {
                    target.find('button').on('click', function () {
                        $(this).attr('disabled', true).text('Соединение...');
                        setTimeout(function () {
                            services.call(target.find('input[type="hidden"]').val())
                                .then(function (result) {
                                    message.success('Запрос отправлен. Ожидайте звонка')
                                })
                                .fail(function () {
                                    message.error('Произошла ошибка. Повторите попытку');
                                })
                                .always(function () {
                                    $('td[data-target="' + target.attr('id') + '"]').webuiPopover('hide')
                                });
                        }, 2000)
                    })
                });
        }
    }

    function _getCalls(request_string, callback) {
        _updateContainer();
        $.get('/getCalls/{0}'.format(request_string || ''), function (data) {
            _updateContainer(data);
        }).fail(function () {
            services.errors().getDefaultErrorPage().success(function (result) {
                _updateContainer(result)
            })
        })
    }

    function _collectData() {
        var data = {};
        var elements = $('input.pseudo-hidden');
        for (var i = 0; i < elements.length; i++) {
            var key = $(elements[i]).attr('name');
            var value = $(elements[i]).attr('value');
            data[key] = Number(value).toString() == 'NaN' ? value : value == 0 ? 2 : value - 1;
        }
        return data;
    }

    $(document).ready(function () {
        _setContainer();
        _initDatepicker();
        _getCalls(new ApiParams().getRequestString());

        var elements = $('switcher');
        for (var i = 0; i < elements.length; i++){
            new Switcher(elements[i]);
        }
    });

    return {
        applyFilters: function () {
            var params = _collectData();
            var request_string = new ApiParams(params).getRequestString();
            _getCalls(request_string);
        }
    };
})();