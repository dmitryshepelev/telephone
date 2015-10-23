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

    function _makeSortable() {
        var table = $('#callsTable');
        if (table && table.children('tbody').children('tr').length > 1) {
            table.tablesorter({sortList: [[1,1]], cssAsc: 'table-sort table-sort-asc', cssDesc: 'table-sort table-sort-desc', textExtraction: function (node) {
                var value = node.innerHTML;
                if (value.search(/(мин|сек)/g) != -1) {
                    var textArr = value.split(' ');
                    value = (textArr.length === 2 ? textArr[0] : Number(textArr[0]) * 60 + Number(textArr[2])).toString();
                }
                return value
            }});
        }
    }

    function _updateContainer(data) {
        if (data){
            _container.append(data);
            _makeSortable();
            mainController.initTooltips();
            _container.showElement();
        } else {
          _container.hideElement(200, function () {
                _container.empty();
            });
        }
    }

    function _getCalls(request_string, callback) {
        _updateContainer();
        loader.show();
        $.get('/getCalls/{0}'.format(request_string || ''), function (data) {
            _updateContainer(data);
            //loader.hide();
        }).fail(function () {
            services.errors().getDefaultErrorPage().success(function (result) {
                _updateContainer(result)
            })
        }).always(function () {
            loader.hide()
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

    //function _getCallRecordLink(callId, onSuccess) {
    //    if (callId) {
    //        $.get('/getCallRecordLink?call_id={0}'.format(callId), function (data) {
    //            services.executeCallback(onSuccess, data)
    //        })
    //    }
    //}
    //
    //function _getCallId(e) {
    //    var attr = 'data-call-id';
    //    var element = $(e.target);
    //    return element.closest('tr[{0}]'.format(attr)).attr(attr);
    //}

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
        //playAction: function (e) {
        //    var callId = _getCallId(e);
        //    console.log(callId);
        //    _getCallRecordLink(callId, function (link) {
        //        console.log(link);
        //    })
        //},
        //downloadRecord: function (e) {
        //    var callId = _getCallId(e);
        //    console.log(callId);
        //    _getCallRecordLink(callId, function (link) {
        //        console.log(link);
        //        window.location.href = link
        //    })
        //}
    };
})();