const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;

let js = fs.readFileSync("too_many_semicolons.js", "utf-8");

const ast = parser.parse(js);

traverse(ast, {
    EmptyStatement: function(path) {
        path.remove();
    }
});

let clean = generate(ast).code;

fs.writeFileSync("clean3.js", clean);
