const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;
const types = require("@babel/types");

let hjs = fs.readFileSync("brackets.js", "utf-8");

const ast = parser.parse(hjs);

traverse(ast, {
    CallExpression: function(path) {
        let prop = path.node.callee.property;

        if (types.isStringLiteral(prop)) {
          path.node.callee.property = types.Identifier(prop.value);
          path.node.callee.computed = false;
        }
    }
});

let clean = generate(ast).code;

fs.writeFileSync("clean2.js", clean);
