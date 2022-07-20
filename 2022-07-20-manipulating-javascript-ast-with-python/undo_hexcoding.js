const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;

let hjs = fs.readFileSync("hexcoded.js", "utf-8");

const ast = parser.parse(hjs);

traverse(ast, {
    StringLiteral: function(path) {
        path.node.extra.raw = "\"" + path.node.extra.rawValue + "\"";
    }
});

let clean = generate(ast).code;

fs.writeFileSync("clean1.js", clean);
