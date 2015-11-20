var $RouteProvider = (function ($) {
    function RouteProvider (states, params) {
        this.$$states = null;
        this.$$params = {
            animate: true
        };

        if (states) {
            this.states.setStates(states)
        }

        this._init(params)
    }

    RouteProvider.prototype = {
        constructor: RouteProvider,

        _init: function (params) {
            for (var param in params) {
                if (params.hasOwnProperty(param)) {
                    this.$$params[param] = params[param];
                }
            }

            if ('onhashchange' in window) {
                var thus = this;
                window.onhashchange = function (e) {
                    var newUrl = e.newURL;
                    var state = thus.states.resolveState(newUrl);
                    if (state) {
                        thus.states.load.call(thus, state)
                    }
                    //console.log(state);
                }
            }
        },

        states: {
            clear: function () {
                this.$$states = null;
            },
            setStates: function (states) {
                this.$$states = states
            },
            getStates: function () {
                return this.$$states
            },
            getState: function (name) {
                return this.$$states[name]
            },
            resolveState: function (url) {
                var urlParts = url.split('#');
                if (urlParts.length === 2) {
                    return this.getState(urlParts[1])
                }
                return null
            },
            load: function (state) {
                var animate = this.$$params.animate;
                $.get(state.controller, function (result) {
                    var container = $('wp-container');
                    container.fadeOut(animate ? 200 : 0, function () {
                        container.empty();
                        container.append(result);
                        container.fadeIn(animate ? 200 : 0);
                        $.getScript(state.scripts[0], function (res) {
                            console.log(res);
                        })
                    });
                    //console.log(result);
                })
            }
        }
    };

    return RouteProvider
})($);
