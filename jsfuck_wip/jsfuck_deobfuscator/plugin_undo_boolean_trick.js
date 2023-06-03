const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "undo-boolean-trick", // not required
    visitor: {
      Identifier(path) {
        let node = path.node;
       	if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (node.name === "Boolean") {
          let newNode = t.valueToNode(String(Boolean));
          logASTChange("undo-boolean-trick", node, newNode);
          path.replaceWith(newNode);
        }
      }
    }
  };
}
