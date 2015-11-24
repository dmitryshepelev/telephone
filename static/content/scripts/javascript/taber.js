var Taber = (function () {
    function Taber (selector, tabs, params) {
        this._element = $(selector || '#taber');
        this._params = {
            defaultActive: 0,
            afterChange: null,
            minContentHeight: null
        };

        this.setParams(params);
        this._taber = $('<div class="taber"></div>');
        this._header = $('<div class="taber-header"></div>');
        this._container = $('<div class="taber-content" ' + (this._params.minContentHeight ? ('style="min-height: ' + this._params.minContentHeight + 'px;"') : '') + '></div>');
        this._tabs = this._initTabs(tabs);
        this._init();
    }

    Taber.prototype = {
        constructor: Taber,

        _consts: {
            tabClass: 'taber-tab',
            activeClass: 'active'
        },

        _init: function () {
            if (!this._element) {
                throw 'Element isn\'t defined';
            }
            var template = this._taber.append(this._header, this._container);
            this._element.after(template);

            var defaultTab = this._tabs[this._params.defaultActive];
            this._toggleActive(defaultTab.element);
            this._updateTabContent(defaultTab.url)
        },

        _updateTabContent: function (url) {
            var thus = this;
            thus._container.setInvisible(200, function () {
                $.get(url, function (data) {
                    thus._cleanContainer();
                    thus._container.append(data);
                    if (thus._params.afterChange) {
                        thus._params.afterChange()
                    }
                    thus._container.setVisible()
                }).fail(function () {
                    thus._container.append('Произошла ошибка')
                })
            });
        },

        _cleanContainer: function () {
            this._container.empty()
        },

        _toggleActive: function (element) {
            var currActive = this._header.children('.{0}.{1}'.format(this._consts.tabClass, this._consts.activeClass));
            currActive.removeClass(this._consts.activeClass);
            element.addClass(this._consts.activeClass);
        },

        _onTabClick: function (e) {
            var jqElement = $(e.target);

            if (jqElement.hasClass(this._consts.activeClass)) {
                return !0;
            }

            var tabName = jqElement.attr('data-name');
            var tab = this._tabs.filter(function (tab) {
                return tab.name == tabName;
            })[0];

            this._toggleActive(jqElement);
            this._updateTabContent(tab.url);
        },

        _initTabs: function (t) {
            var tabs = [];
            for (var i = 0; i < t.length; i++) {
                var tab = {
                    name: t[i].name || '',
                    url: t[i].url,
                    element: $('<div id="tab-' + i + '" class="' + this._consts.tabClass +' ' + (t[i].isActive || i == Number(this._params.defaultActive) ? this._consts.activeClass : '') + '" data-name="' + t[i].name + '">' + t[i].name + '</div>')
                        .on('click', this._onTabClick.bind(this))
                };
                this._header.append(tab.element);
                tabs.push(tab);
            }
            return tabs;
        },

        setParams: function (params) {
            for(var param in params) {
                if (params.hasOwnProperty(param)) {
                    this._params[param] = params[param];
                }
            }
        }
    };

    return Taber;
})();