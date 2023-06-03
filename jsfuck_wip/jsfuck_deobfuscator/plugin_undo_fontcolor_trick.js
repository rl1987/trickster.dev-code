const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

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
             let newNode = t.valueToNode(String.prototype.fontcolor());
             logASTChange("undo-fontcolor-trick", node, newNode);
             path.replaceWith(newNode);
           } else if (t.isLiteral(node.arguments[0])) {
             let newNode = t.valueToNode(String.prototype.fontcolor(node.arguments[0].value));
             logASTChange("undo-fontcolor-trick", node, newNode);
             path.replaceWith(newNode);
           }
        }
      }
    }
  };
}
