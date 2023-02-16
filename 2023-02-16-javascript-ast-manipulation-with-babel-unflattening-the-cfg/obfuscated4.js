function a(c, f) {
  var b = new Array(2);
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
        function e() {
          var _a = arguments[0],
              _c = Array.prototype.slice.call(arguments, 1);

          var _b = function () {
            return _a.apply(this, _c.concat(Array.prototype.slice.call(arguments)));
          };

          _b.prototype = _a.prototype;
          return _b;
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