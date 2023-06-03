const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
 return {
    name: "number-constructor-str", // not required
    visitor: {
      MemberExpression(path) {
        const node = path.node;
        let obj = node.object;
        if (!t.isNumericLiteral(obj)) return;
        let property = node.property;
        if (!t.isStringLiteral(property)) return;
        if (property.value != "constructor") return;
        if (!t.isBinaryExpression(path.parent)) return;
        
        let newNode = t.stringLiteral(String(Number.prototype.constructor));
        logASTChange("number-constructor-str", node, newNode);
        path.replaceWith(newNode);
      }
    }
  };
}
