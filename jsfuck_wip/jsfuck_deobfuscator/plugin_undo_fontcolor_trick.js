const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
  return {
    name: "undo-fontcolor-trick", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isStringLiteral(node.callee.object)) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value === "fontcolor") {
           if (node.arguments.length === 0) {
             path.replaceWith(t.valueToNode(String.prototype.fontcolor()));
           } else if (t.isLiteral(node.arguments[0])) {
             path.replaceWith(t.valueToNode(String.prototype.fontcolor(node.arguments[0].value)))
           }
        }
      }
    }
  };
}
