const fs = require("fs");

const parser = require("@babel/parser");
const generate = require("@babel/generator").default;
const traverse = require("@babel/traverse").default;
const types = require("@babel/types");

let code = fs.readFileSync("obfuscated.js", "utf-8");

const ast = parser.parse(code);

traverse(ast, {
    MemberExpression: function(path) {
        if (!path.node.property) return;
        if (!types.isNumericLiteral(path.node.property)) return;

        let idx = path.node.property.value;

        let binding = path.scope.getBinding(path.node.object.name);
        if (!binding) return;
        
        if (types.isVariableDeclarator(binding.path.node)) {
            let array = binding.path.node.init;
            if (idx >= array.length) return;

            let member = array.elements[idx];

            if (types.isStringLiteral(member)) {
                path.replaceWith(member);
            }
        }
    }
});

fs.writeFileSync("clean.js", generate(ast).code);

