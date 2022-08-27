function dead1(a, b) {
    return a + b + 1;
}

function dead2() {
    console.log("!!");
}

function dead3() {
    dead1(1, 2);
    dead2();
}

console.log("Hello");
