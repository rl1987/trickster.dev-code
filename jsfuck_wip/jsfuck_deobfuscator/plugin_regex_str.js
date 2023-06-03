const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "regex-str", // not required
    visitor: {
      BinaryExpression(path) {
        const binExpr = path.node;
        const left = binExpr.left;
        if (!t.isRegExpLiteral(left)) return;
        const right = binExpr.right;
        if (!t.isArrayExpression(right)) return;
        if (right.elements.length != 0) return;
        
        const regexStr = String(RegExp(left.pattern));
        
        let newNode = t.stringLiteral(regexStr);
        logASTChange("regex-str", node, newNode);
        path.replaceWith(newNode);
      }
    }
  };
}
