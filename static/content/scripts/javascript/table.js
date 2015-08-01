var table = (function () {
    var tableIds = {
        table: 'table',
        header: 'theader',
        body: 'tbody'
    };



    return {
        fillTable: function (values, excludeIndexesArray) {
            var columns = ['Время', 'Откуда', 'Продолжительность звонка', 'Продолжительность разговора', 'ID записи'];
            var body = $('#' + tableIds.body);
            var template = '<td id="val">val</td>';
            values.forEach(function (value, index) {
                body.append('<tr><td>' + (index + 1) + '</td></tr>');
                var contentRow = $('#' + tableIds.body + ' tr:last-child');
                for (var v in value) {
                    var valueIndex = columns.indexOf(v);
                    if (valueIndex !== -1) {
                        var valueToInsert = value[v];
                        if (valueIndex === 2 || valueIndex === 3) {
                            var time = converter.fromSeconds(valueToInsert);
                            valueToInsert = (time[0] > 0 ? time[0] + ' мин ' : '') + (time[1] + ' сек');
                        }
                        contentRow.append(template.replace(/val/g, valueToInsert));
                    }
                }
            })
        }
    }
})();
