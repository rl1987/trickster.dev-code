(function () {
    function a(a, d) {
        var b = new Array(0);;
        var c = arguments;
        while (true)
            try {
                switch (a) {
                case 15229:
                    return;
                case 21176:
                    function e(a, b) {
                        return Array.prototype.slice.call(a).concat(Array.prototype.slice.call(b));
                    }
                    function f() {
                        var a = arguments[0], c = Array.prototype.slice.call(arguments, 1);
                        var b = function () {
                            return a.apply(this, c.concat(Array.prototype.slice.call(arguments)));
                        };
                        b.prototype = a.prototype;
                        return b;
                    }
                    function g(a, b) {
                        return Array.prototype.slice.call(a, b);
                    }
                    function h(b) {
                        var c = {};
                        for (var a = 0; a < b.length; a += 2) {
                            c[b[a]] = b[a + 1];
                        }
                        return c;
                    }
                    function i(a) {
                        return a.map(function (a) {
                            return String.fromCharCode(a & ~0 >>> 16) + String.fromCharCode(a >> 16);
                        }).join('');
                    }
                    function j() {
                        return String.fromCharCode.apply(null, arguments);
                    }
                    console.log('Hello, world! ' + 123);
                    a = 15229;
                    break;
                }
            } catch (b) {
                $$defendjs$tobethrown = null;
                switch (a) {
                default:
                    throw b;
                }
            }
    }
    a(21176, {});
}())