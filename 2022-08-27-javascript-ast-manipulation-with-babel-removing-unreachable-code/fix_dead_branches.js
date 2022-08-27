const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;
const types = require("@babel/types");

let js = fs.readFileSync("dead_branches.js", "utf-8");

const ast = parser.parse(js);

traverse(ast, {
    "ConditionalExpression|IfStatement": function(path) {
        let isTruthy = path.get("test").evaluateTruthy();
        let node = path.node;

        if (isTruthy) {
            if (types.isBlockStatement(node.consequent)) {
                path.replaceWithMultiple(node.consequent.body);
            } else {
                path.replaceWith(node.consequent);
            }
        } else if (node.alternate != null) {
            if (types.isBlockStatement(node.alternate)) {
                path.replaceWithMultiple(node.alternate.body);
            } else {
                path.replaceWith(node.alternate);
            }
        } else {
            path.remove();
        }
    }
});

let clean = generate(ast).code;

fs.writeFileSync("no_dead_branches.js", clean);
