var services = (function () {
    /**
     * Sets data to the '_data' private property of the class.
     * Create new private property '_data' if it doesn't exist
     * @param data to set
     * @private
     */
    function _setData(data) {
        if (!this.hasOwnProperty('_data')) {
            this._data = {};
        }
        for (var d in data) {
            if (data.hasOwnProperty(d)) {
                this._data[d] = data[d]
            }
        }
    }

    /**
     * Collect data from html page based on class model
     * @param model
     * @returns {{data: {}, errors: Array}} data object, array of names of the errors properties
     * @private
     */
    function _collectModelData(model) {
        var result = {
            data: {},
            errors: []
        };
        for (var m in model) {
            if(model.hasOwnProperty(m)) {
                var element = $('#' + model[m]);
                result.data[m] = element[0].value;
                if (!!element.attr('required') && !result.data[m]) {
                    result.errors.push(m)
                }
            }
        }
        return result
    }

    /**
     * Clean data in html page based on the class model
     * @param model
     * @param onClean callback to execute when data will be cleared
     * @private
     */
    function _cleanModelData(model, onClean) {
        for (var m in model) {
            if (model.hasOwnProperty(m)) {
                $('#' + model[m]).val('');
            }
        }
        _executeCallback(onClean);
    }

    /**
     * Generate params string as 'param1=value&param2=value...' from object
     * @param data
     * @returns {string}
     * @private
     */
    function _getParamsString(data) {
        var str = '';
        for(var d in data) {
            if (data.hasOwnProperty(d)) {
                str += '{0}={1}&'.format(d, data[d])
            }
        }
        return str.slice(0, -1)
    }

    /**
     * Create instance on the class
     * The first argument is class constructor. Required
     * The second argument is data to fill class instance. If the second is missed, class with default values will be created.
     * Else if the second is falsy then data to fill class will be collected form html page based on class model.
     * @returns {cls} instance of cls class
     * @private
     */
    function _createInstance() {
        var errorTitle = 'CrInsErr.';
        var cls = arguments[0];
        var instance = new cls;
        if (!cls.prototype.setData) {
             cls.prototype.setData = _setData;
        }
        if (arguments.length > 1) {
            var data = arguments[1];
            if (!data) {
                if (cls.prototype.hasOwnProperty('getModel')) {
                    var collectedData = _collectModelData(cls.prototype.getModel());
                    data = collectedData.data;
                    instance.creationErrors = collectedData.errors.length > 0 ? collectedData.errors : null
                } else {
                    throw '{0} Class hasn\'t model. Ensure that class \'{1}\' has \'getModel()\' method'.format(errorTitle, cls.name);
                }
            }
            instance.setData(data);
        }
        return instance
    }

    /**
     * Execute callback function with params array
     * @param callback function
     * @param params array
     * @private
     */
    function _executeCallback(callback, params) {
        if (callback) {
            callback(params)
        }
    }

    /**
     * Service to get urls to api access
     * @returns {{OAuthCodeUrl: Function}}
     * @private
     */
    function _getApiUrls() {
        var _baseUrl = '/services/getApiUrls?reason={0}';

        /**
         * Execute GET request to the server
         * @param url
         * @private
         */
        function _executeGetRequest(url) {
            return $.get(url)
        }

        return {
            /**
             * Get url to get OAuth code
             */
            OAuthCodeUrl: function () {
                var url = _baseUrl.format('OAuthCode');
                return _executeGetRequest(url);
            }
        }
    }

    /**
     * Validate html element by its id
     * @param elementId string
     * @param isValid leave undefined or set false value to make element invalid
     * @private
     */
    function _validate (elementId, isValid) {
        var errorCss = 'error';
        var element = $('#' + elementId);
        if (isValid == true) {
            element.removeClass(errorCss);
        } else {
            element.addClass(errorCss);
            element.on('change', _validate.bind(this, elementId, true))
        }
    }

    /**
     * Bind key pressed
     * @param key keyname to bind
     * @param handler to execute
     * @private
     */
    function _bindKey (key, handler) {
        var keyMatch = [
            { name: 'enter', code: 13 }
        ];
        var keyToBind = keyMatch.filter(function (k) {
            return k.name == key
        })[0];
        if (keyToBind) {
            $(document).keypress(function (e) {
                if (e.which == keyToBind.code) {
                    _executeCallback(handler)
                }
            })
        }
    }

    /**
     * Gets error pagers
     * @returns {{getDefaultErrorPage: Function}}
     * @private
     */
    function _errors () {
        var baseUrl = '/services/e/';
        return {
            getDefaultErrorPage: function () {
                return $.get(baseUrl)
            }
        }
    }

    /**
     * Make table sortable
     * @param selector to define table
     * @param sortList sort start queue
     * @param textExtraction text extraction function
     * @private
     */
    function _makeSortable(selector, sortList, textExtraction) {
        var table = $(selector);
        if (table && table.children('tbody').children('tr').length > 1) {
            table.tablesorter({
                sortList: sortList,
                cssAsc: 'table-sort table-sort-asc',
                cssDesc: 'table-sort table-sort-desc',
                textExtraction: function (node) {
                    var value = node.innerHTML;
                    if (value.search(/(мин|сек)/g) != -1) {
                        var textArr = value.split(' ');
                        value = (textArr.length === 2 ? textArr[0] : Number(textArr[0]) * 60 + Number(textArr[2])).toString();
                        return value
                    }
                    var re = new RegExp(/((\d{2}\.){2}\d{4})\s((\d{2}\.){2}\d{2})/g);
                    var match = value.match(re);
                    if (match) {
                        var arr = match[0].split(/\.|\s/);
                        var date = new Date(arr[2], arr[1] - 1, arr[0], arr[3], arr[4], arr[5]);
                        return date.getTime() / 1000;
                    }
                    if (textExtraction) {
                        value = textExtraction(node);
                    }
                    return value
                }
            });
        }
    }

    /**
     * Function to operate with table data
     * @param selector to define table
     * @returns {{searchRows: Function}}
     */
    function _filterTable (selector) {
        var table = $(selector);
        var colNumber = table.find('th').length;
        var body = table.children('tbody');
        var emptyRow = $('<tr id="emptyRow" style="display: none"><td colspan={0}>Нет совпадений</td></tr>'.format(colNumber));
        return {
            /**
             * Search row in the table by target value
             * To allow searching in the row, add {allow-search} tag to <td>
             * @param value to search
             * @returns the number of the founded rows
             */
            searchRows: function (value) {
                $('#emptyRow').remove();
                var re = new RegExp(value);
                var rows = body.children('tr');
                var rowsFound = 0;
                $.each(rows, function (index, row) {
                    row = $(row);
                    var sourceCells = row.children('td[allow-search]');
                    var targetCells = sourceCells.filter(function (index, cell) {
                        return $(cell).text().match(re);
                    });
                    if (targetCells.length == 0) {
                        row.hideElement();
                    } else {
                        row.showElement();
                        rowsFound++
                    }
                });
                if (rowsFound === 0) {
                    body.append(emptyRow);
                    emptyRow.showElement();
                }
                return rowsFound;
            }
        }
    }

    /**
     * Create and show modal instance
     * @param template template name to fill modal content
     * @param params modal content params
     * @param onShown callback is executed after modal is shown to the user
     * @param onHidden callback is executed after modal is hidden
     */
    function _modal (template, params, onShown, onHidden) {
        var _id = 'modal';
        var modal = $('<div id="' + _id + '" class="modal fade" tabindex="-1" role="dialog">' +
	                    '<div class="modal-dialog">' +
		                    '<div class="modal-content">' +
		                    '</div>' +
	                    '</div>' +
                      '</div>');
        modal.on('hidden.bs.modal', function () {
            $('#' + _id).remove();
            services.executeCallback(onHidden, modal)
        });
        modal.on('shown.bs.modal', function () {
            $('[autofocus]').focus();
            services.executeCallback(onShown, modal)
        });
        $(document.body).append(modal);

        var paramsString = this.getParamsString(params);
        $('#' + _id).modal({
            backdrop: 'static',
            remote: '/services/getmodal/' + template + '/?' + paramsString
        });
    }

    return {
        collectModelData: _collectModelData,
        cleanModelData: _cleanModelData,
        getParamsString: _getParamsString,
        createInstance: _createInstance,
        executeCallback: _executeCallback,
        getApiUrls: _getApiUrls,
        validate: _validate,
        bindKey: _bindKey,
        errors: _errors,
        makeSortable: _makeSortable,
        filterTable: _filterTable,
        modal: _modal
    }
})();