const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-regexp-trick", // not required
    visitor: {
      Identifier(path) {
        let node = path.node;
       	if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (node.name === "RegExp") {
          let newNode = t.valueToNode(String(RegExp));
          logASTChange("undo-regexp-trick", node, newNode);
          path.replaceWith(newNode);
        }
      },
      CallExpression(path) {
        let node = path.node;
        if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (!t.isIdentifier(node.callee)) return;
        if (node.callee.name != "RegExp") return;
        if (node.arguments.length === 0) {
          let newNode = t.valueToNode(String(RegExp()));
          logASTChange("undo-regexp-trick", node, newNode);
          path.replaceWith(newNode);
        } else if (node.arguments.length === 1 &&
                   t.isStringLiteral(node.arguments[0]) &&
                   node.arguments[0].value === "/") {
          let newNode = t.valueToNode(String(RegExp("/")));
          logASTChange("undo-regexp-trick", node, newNode);
          path.replaceWith(newNode);
        }
      }
    }
  };
}
