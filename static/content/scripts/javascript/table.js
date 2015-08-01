var table = (function () {
    var tableIds = {
        table: 'table',
        header: 'theader',
        body: 'tbody'
    };

    /**
     * Fill the row of the table with values of the object
     * @param rowElement - DOM element to fill
     * @param valuesObj - object with values to fill
     * @param template - HTML template with 'val' to replace with value
     * @param excludeIndexes - exclude some values by their indexes. Starts from 1.
     */
    function fillRow (rowElement, valuesObj, template, isHeader, excludeIndexes) {
        var index = 1;
        for (var value in valuesObj) {
            if (excludeIndexes && !excludeIndexes.filter(function (i) {
                    return i === index;
                })[0]) {
                rowElement.append(template.replace(/val/g, isHeader ? value : valuesObj[value]));
            }
            index++;
        }
    }

    return {
        generateTable: function (container) {
            var template =
                '<table id="' + tableIds.table + '" class="table table-striped table-hover">' +
                    '<thead id="' + tableIds.header + '" >' +
                        '<tr>' +
                        '</tr>' +
                    '</thead>' +
                    '<tbody id="' + tableIds.body + '">' +
                    '</tbody>' +
                '</table>';
            container.append(template);
            return tableIds;
        },

        /**
         * generateHeader
         * @param valuesObj - object of header labels names
         * @param excludeIndexesArray - array of indexes to exclude from header. Starts from 1.
         */
        generateHeader: function (valuesObj, excludeIndexesArray) {
            var headerRow = $('#' + tableIds.header + ' tr');
            var template = '<th>val</th>';
            fillRow(headerRow, valuesObj, template ,true, excludeIndexesArray);
        },

        fillTable: function (values, excludeIndexesArray) {
            var body = $('#' + tableIds.body);
            var template = '<td>val</td>';
            values.forEach(function (value) {
                body.append('<tr></tr>');
                var contentRow = $('#' + tableIds.body + ' tr:last-child');
                fillRow(contentRow, value, template, false, excludeIndexesArray);
            })
        }
    }
})();
