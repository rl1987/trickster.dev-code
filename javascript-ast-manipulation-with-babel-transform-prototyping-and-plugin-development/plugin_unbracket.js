const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
    return {
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
    }
};
