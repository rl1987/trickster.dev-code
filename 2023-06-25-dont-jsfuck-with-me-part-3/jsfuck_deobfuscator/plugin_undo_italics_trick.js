const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-italics-trick", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isStringLiteral(node.callee.object)) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value === "italics") {
           const fromStr = node.callee.object.value;
           if (node.arguments.length === 0) {
             let newNode = t.valueToNode(fromStr.italics());
             logASTChange("undo-italics-trick", node, newNode);
             path.replaceWith(newNode);
           } 
        }
      }
    }
  };
}
