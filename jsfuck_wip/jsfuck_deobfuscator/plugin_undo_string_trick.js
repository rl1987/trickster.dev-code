const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-string-trick", // not required
    visitor: {
      Identifier(path) {
        let node = path.node;
       	if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (node.name === "String") {
          let newNode = t.valueToNode(String(String));
          logASTChange("undo-string-trick", node, newNode);
          path.replaceWith(newNode);
        }
      }
    }
  };
}
