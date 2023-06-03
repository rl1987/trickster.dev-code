const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-function-escape-trick", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (t.isCallExpression(node.callee) &&
            t.isCallExpression(node.callee.callee) &&
            t.isIdentifier(node.callee.callee.callee) &&
            node.callee.callee.callee.name === "Function" &&
            node.callee.callee.arguments.length === 1 &&
            t.isStringLiteral(node.callee.callee.arguments[0]) &&
            node.callee.callee.arguments[0].value === "return escape" &&
            t.isStringLiteral(node.arguments[0])
           ) {
          let newNode = t.valueToNode(escape(node.arguments[0].value));
          logASTChange("undo-function-escape-trick", node, newNode);
          path.replaceWith(newNode);
        }
      }
    }
  };
}
