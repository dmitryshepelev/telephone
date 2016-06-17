var Switcher = (function () {
    function Switcher (element) {
        this._element = $(element);
        this._params = {
            name: '',
            value: 0,
            titles: [],
        };

        var _hiddenElementTemplate = '<input type="hidden" class="pseudo-hidden" name="{0}" value="{1}" />';
        var _template = '<div class="switcher-container"><div class="switcher"></div></div>';
        var _labelTemplate = '<span class="switcher-label"></span>';

        for (var i = 0; i < element.attributes.length; i++) {
            this._params[element.attributes[i].name] = element.attributes[i].value;
        }
        this._element.after(_hiddenElementTemplate.format(this._params.name, this._params.value));
        this._element.append(_template);
        this._element.parent().append(_labelTemplate);
        this._element.on('click', this.toggle.bind(this));

        this.toggle();
    }

    Switcher.prototype = {
        constructor: Switcher,
        _setValue: function () {
            this._params.value = this._params.value < 2 ? this._params.value + 1 : 0;
            this._element.attr('value', this._params.value);
            this._element.next().val(this._params.value);
        },
        _changeColor: function () {
            var bgColor = '';
            switch (this._params.value) {
                case 0:
                    bgColor = '#1ABB9C';
                    break;
                case 1:
                    bgColor = '#DDDDDD';
                    break;
                case 2:
                    bgColor = '#D9534F';
                    break;
                default: throw 'Unexpected value {0}'.format(this._params.value);
            }
            $(this._element).css('background-color', bgColor);
        },
        _move: function () {
            this._element.find('.switcher').css('left', ((this._params.value / 4) * 100) + '%');
        },
        _updateLabel: function () {
            var labels = [];
            try {
                labels = eval(this._params.titles);
            } catch (e) {
                throw 'Switcher labels error: {0}'.format(this._params.titles);
            }
            var label = labels instanceof Array ? labels[this._params.value] : 'string' === typeof labels ? labels : 'Label error';
            this._element.siblings('.switcher-label').text(label);
        },
        toggle: function () {
            this._setValue();
            this._changeColor();
            this._move();
            this._updateLabel();
        }
    };

    return Switcher
})();