(function () {
    {
        {
            function b(a, b) {
                return Array.prototype.slice.call(a).concat(Array.prototype.slice.call(b));
            }
            function c() {
                var a = arguments[0], c = Array.prototype.slice.call(arguments, 1);
                var b = function () {
                    return a.apply(this, c.concat(Array.prototype.slice.call(arguments)));
                };
                b.prototype = a.prototype;
                return b;
            }
            function d(a, b) {
                return Array.prototype.slice.call(a, b);
            }
            function e(b) {
                var c = {};
                for (var a = 0; a < b.length; a += 2) {
                    c[b[a]] = b[a + 1];
                }
                return c;
            }
            function f(a) {
                return a.map(function (a) {
                    return String.fromCharCode(a & ~0 >>> 16) + String.fromCharCode(a >> 16);
                }).join('');
            }
            function g() {
                return String.fromCharCode.apply(null, arguments);
            }
        }
        var a = [];
        a[0] = 10;
        a[1] = 20;
        a[2] = 30;
        console.log(a[0] + a[2]);
        console.log(a[0] + a[1]);
    }
}())