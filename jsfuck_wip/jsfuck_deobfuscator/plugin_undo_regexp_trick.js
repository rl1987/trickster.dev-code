const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
  return {
    name: "undo-regexp-trick", // not required
    visitor: {
      Identifier(path) {
        let node = path.node;
       	if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (node.name === "RegExp") path.replaceWith(t.valueToNode(String(RegExp)));
      },
      CallExpression(path) {
        let node = path.node;
        if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (!t.isIdentifier(node.callee)) return;
        if (node.callee.name != "RegExp") return;
        if (node.arguments.length === 0) {
          path.replaceWith(t.valueToNode(String(RegExp())));
        } else if (node.arguments.length === 1 &&
                   t.isStringLiteral(node.arguments[0]) &&
                   node.arguments[0].value === "/") {
          path.replaceWith(t.valueToNode(String(RegExp("/"))));
        }
      }
    }
  };
}
