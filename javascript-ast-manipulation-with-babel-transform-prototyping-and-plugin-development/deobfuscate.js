const fs = require("fs");
const path = require("path");

const babel = require("@babel/core");
const t = require("@babel/types");

const result = babel.transformFileSync(path.join(__dirname, 'input.js') , {
    plugins: [{
        name: "undo_hexadecimal_strings",
        visitor: {
            StringLiteral: function (path) {
                path.node.extra.raw = '"' + path.node.extra.rawValue + '"';
            }
        }
    }, {
        name: "bracket_to_dot",
        visitor: {
            CallExpression: function (path) {
                let prop = path.node.callee.property;

                if (t.isStringLiteral(prop)) {
                    path.node.callee.property = t.Identifier(prop.value);
                    path.node.callee.computed = false;
                }
            }
        }
    }, {
        name: "rm_needless_semicolons",
        visitor: {
            EmptyStatement: function (path) {
                path.remove();
            }
        }
    }]
});

console.log(result.code);

fs.writeFileSync(path.join(__dirname, 'output.js'), result.code, 'utf-8');

