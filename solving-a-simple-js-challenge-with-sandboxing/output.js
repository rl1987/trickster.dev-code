function leastFactor(n) {
  if (isNaN(n) || !isFinite(n)) return NaN;
  if (typeof phantom !== 'undefined') return 'phantom';
  if (typeof module !== 'undefined' && module.exports) return 'node';
  if (n == 0) return 0;
  if (n % 1 || n * n < 2) return 1;
  if (n % 2 == 0) return 2;
  if (n % 3 == 0) return 3;
  if (n % 5 == 0) return 5;
  var m = Math.sqrt(n);

  for (var i = 7; i <= m; i += 30) {
    if (n % i == 0) return i;
    if (n % (i + 4) == 0) return i + 4;
    if (n % (i + 6) == 0) return i + 6;
    if (n % (i + 10) == 0) return i + 10;
    if (n % (i + 12) == 0) return i + 12;
    if (n % (i + 16) == 0) return i + 16;
    if (n % (i + 22) == 0) return i + 22;
    if (n % (i + 24) == 0) return i + 24;
  }

  return n;
}

function go() {
  var p = 620948551137797;
  var s = 2221541592;
  var n;
  if (s >> 7 & 1) p += 229368228 * 8;else p -= 193278138 * 8;
  if (s >> 2 & 1) p += 396865909 * 5;else p -= 4569197 * 3;
  if (s >> 11 & 1) p += 48259709 * 12;else p -= 104005356 * 12;
  if (s >> 1 & 1) p += 887348560 * 2;else p -= 521276949 * 2;
  if (s >> 8 & 1) p += 45635489 * 11;else p -= 233901153 * 9;
  p -= 543022206;
  n = leastFactor(p);
  {
    document.cookie = "KEY=" + n + "*" + p / n + ":" + s + ":3373455379:1;path=/;";
    document.location.reload(true);
  }
}
