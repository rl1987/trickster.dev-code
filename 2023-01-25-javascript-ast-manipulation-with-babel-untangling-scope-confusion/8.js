(function () {
  {
    {
      function b(a, b) {
        return Array.prototype.slice.call(a).concat(Array.prototype.slice.call(b));
      }

      function c() {
        var a = arguments[0],
            c = Array.prototype.slice.call(arguments, 1);

        var b = function () {
          return a.apply(this, c.concat(Array.prototype.slice.call(arguments)));
        };

        b.prototype = a.prototype;
        return b;
      }
    }
    var a = [];
    a[0] = 10;
    a[1] = 20;
    a[2] = 30;
    console.log(a[0] + a[2]);
    console.log(a[0] + a[1]);
  }
})();