(function () {
    function c() {
        var c = arguments;
        var b = [];
        b[1] = '';
        b[1] += a(72);
        b[1] += a(101, 108, 108, 111);
        b[1] += a(44, 32, 119, 111);
        b[1] += a(114, 108, 100, 33);
        b[1] += a(32);
        return b[1];
    }
    {
        {
            function e(a, b) {
                return Array.prototype.slice.call(a).concat(Array.prototype.slice.call(b));
            }
            function d() {
                var a = arguments[0], c = Array.prototype.slice.call(arguments, 1);
                var b = function () {
                    return a.apply(this, c.concat(Array.prototype.slice.call(arguments)));
                };
                b.prototype = a.prototype;
                return b;
            }
            function f(a, b) {
                return Array.prototype.slice.call(a, b);
            }
            function g(b) {
                var c = {};
                for (var a = 0; a < b.length; a += 2) {
                    c[b[a]] = b[a + 1];
                }
                return c;
            }
            function h(a) {
                return a.map(function (a) {
                    return String.fromCharCode(a & ~0 >>> 16) + String.fromCharCode(a >> 16);
                }).join('');
            }
            function a() {
                return String.fromCharCode.apply(null, arguments);
            }
        }
        var b = [];
        console.log(d(c, b)() + 123);
    }
}())
