const babel = require("@babel/core");
const t = require("@babel/types");

module.exports = function (babel) {
  return {
    name: "string-constructor-name", // not required
    visitor: {
      MemberExpression(path) {
        const outerMembExpr = path.node;
        const innerMembExpr = outerMembExpr.object;
        if (!t.isMemberExpression(innerMembExpr)) return;
        const innerProp = innerMembExpr.property;
        if (!t.isStringLiteral(innerProp)) return;
        if (innerProp.value != "constructor") return;
        const outerProp = outerMembExpr.property;
        if (!t.isStringLiteral(outerProp)) return;
        if (outerProp.value != "name") return;
        
        path.replaceWith(t.stringLiteral("String"));
      }
    }
  };
}
