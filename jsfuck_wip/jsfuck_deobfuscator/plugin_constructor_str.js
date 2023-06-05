const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
 return {
    name: "constructor-str", // not required
    visitor: {
      MemberExpression(path) {
        const node = path.node;
        let obj = node.object;
        let property = node.property;
        if (!t.isStringLiteral(property)) return;
        if (property.value != "constructor") return;
        if (!t.isBinaryExpression(path.parent)) return;
        
        let newNode;
        
        if (t.isNumericLiteral(obj)) {
          newNode = t.stringLiteral(String(Number.prototype.constructor));
        } else if (t.isStringLiteral(obj)) {
          newNode = t.stringLiteral(String(String.prototype.constructor));
        } else if (t.isBooleanLiteral(obj)) {
          newNode = t.stringLiteral(String(Boolean.prototype.constructor));
        }
        
        path.replaceWith(newNode);
      }
    }
  };
}
