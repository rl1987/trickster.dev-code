function a(c, f) {
  var b = new Array(2);
  ;
  var d = arguments;

  while (true) {
    switch (c) {
      case 4678:
        b[2] = d[2];

        if (b[2] === 0 || b[2] === 1) {
          return 1;
        } else {
          return b[2] * d[1][0](b[2] - 1);
        }

        c = 24586;
        break;

      case 24586:
        return;

      case 3865:
        function g(a, b) {
          return Array.prototype.slice.call(a).concat(Array.prototype.slice.call(b));
        }

        function e() {
          var a = arguments[0],
              c = Array.prototype.slice.call(arguments, 1);

          var b = function () {
            return a.apply(this, c.concat(Array.prototype.slice.call(arguments)));
          };

          b.prototype = a.prototype;
          return b;
        }

        function h(a, b) {
          return Array.prototype.slice.call(a, b);
        }

        function i(b) {
          var c = {};

          for (var a = 0; a < b.length; a += 2) {
            c[b[a]] = b[a + 1];
          }

          return c;
        }

        function j(a) {
          return a.map(function (a) {
            return String.fromCharCode(a & ~0 >>> 16) + String.fromCharCode(a >> 16);
          }).join('');
        }

        function k() {
          return String.fromCharCode.apply(null, arguments);
        }

        b[0] = e(a, 4678, b);
        b[1] = 0;

        while (b[1] < 10) {
          console.log(b[1] + '! = ' + b[0](b[1]));
          b[1]++;
        }

        c = 24586;
        break;
    }
  }
}

a(3865, {});