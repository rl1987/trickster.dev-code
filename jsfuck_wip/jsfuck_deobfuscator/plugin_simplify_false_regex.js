const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
  return {
    name: "simplify-false-regex", // not required
    visitor: {
      CallExpression(path) {
        const callExpr = path.node;
        if (callExpr.arguments.length != 0) return;
        if (!t.isCallExpression(callExpr.callee)) return;
        const calleeMemberExpr = callExpr.callee.callee;
        if (!t.isMemberExpression(calleeMemberExpr)) return;
        const memberExpr2 = calleeMemberExpr.object;
        if (!t.isMemberExpression(memberExpr2)) return;
        const arrayObj = memberExpr2.object;
        if (!t.isArrayExpression(arrayObj)) return;
        if (arrayObj.elements.length != 0) return;
        const property1 = memberExpr2.property;
        if (!t.isStringLiteral(property1)) return;
        if (property1.value != "flat") return;
        const property2 = calleeMemberExpr.property;
        if (!t.isStringLiteral(property2)) return;
        if (property2.value != "constructor") return;
        if (callExpr.callee.arguments.length != 1) return;
        const argStrLiteral = callExpr.callee.arguments[0];
        if (!t.isStringLiteral(argStrLiteral)) return;
        if (argStrLiteral.value != "return/false/") return;      
        path.replaceWith(t.regExpLiteral('false', ''));
      }
    }
  };
}
