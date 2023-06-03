const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
  return {
    name: "undo-number-tostring-trick", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isNumericLiteral(node.callee.object)) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value != "toString") return;
        if (node.arguments.length != 1) return;
        if (!t.isLiteral(node.arguments[0])) return;
        
        let numericStr = node.callee.object.value["toString"](node.arguments[0].value);
        path.replaceWith(t.valueToNode(numericStr));
      }
    }
  };
}
