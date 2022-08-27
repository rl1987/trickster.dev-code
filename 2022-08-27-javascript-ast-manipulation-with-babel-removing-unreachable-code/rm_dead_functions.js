const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;
const types = require("@babel/types");

var js = fs.readFileSync("dead_functions.js", "utf-8");
var ast;

do {
    ast = parser.parse(js);
    var removed = 0;
    traverse(ast, {
        FunctionDeclaration: function(path) {
            if (!path.scope.getBinding(path.node.id.name).referenced) {
                path.remove();
                removed++;
            }
        }
    });
    js = generate(ast).code;
} while (removed > 0);

let clean = generate(ast).code;

fs.writeFileSync("no_dead_functions.js", clean);
