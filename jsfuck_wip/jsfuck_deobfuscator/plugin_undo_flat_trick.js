const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-flat-trick", // not required
    visitor: {
      MemberExpression(path) {
        let node = path.node;
        if (!t.isArrayExpression(node.object)) return;
        if (node.object.elements.length != 0) return;
        if (!t.isStringLiteral(node.property)) return;
        if (node.property.value === "flat" && t.isBinaryExpression(path.parent)) {
          let newNode = t.stringLiteral(String(Array.prototype.flat));
          logASTChange("undo-flat-trick", node, newNode);
          path.replaceWith(newNode);
        }
      }
    }
  };
}
