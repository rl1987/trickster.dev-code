const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

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
        let newNode = t.valueToNode(numericStr);
        logASTChange("undo-number-tostring-trick", node, newNode);
        path.replaceWith(newNode);
      }
    }
  };
}
