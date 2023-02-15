function factorial(n) {
  if (n === 0 || n === 1) {
    return 1;
  } else {
    return n * factorial(n - 1);
  }
}

for (let i = 0; i < 10; i++) {
  console.log(i + "! = " + factorial(i));
}
