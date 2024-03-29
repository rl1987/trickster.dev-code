const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "string-array-join", // not required
    visitor: {
      CallExpression(path) {
        // We call cloneNode() to make a copy we could edit without messing up
        // the original subtree that we may want to inspect for debugging.
        const callExpr = t.cloneNode(path.node);
        const memberExpr = callExpr.callee;
        if (!t.isMemberExpression(memberExpr)) return;
        let array = memberExpr.object;
        if (!t.isArrayExpression(array)) return;
        if (array.elements.length == 0) return;
        array = array.elements;

        for (let i = 0; i < array.length; i++) {
          const element = array[i];
          if (!t.isStringLiteral(element))
            return;
          
          array[i] = element.value;
        }
                
        const fnName = memberExpr.property;
        if (!t.isStringLiteral(fnName)) return;
        if (fnName.value != "join") return;
        
        if (callExpr.arguments.length != 1) return;
        
        let separator = callExpr.arguments[0];
        if (!t.isStringLiteral(separator)) return;
        separator = separator.value;
        
        let joinedStr = array.join(separator);
        let newNode = t.stringLiteral(joinedStr);
        logASTChange("string-array-join", path.node, newNode);
        path.replaceWith(newNode);
      }
    }
  };
}
