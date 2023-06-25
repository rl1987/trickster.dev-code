export default function (babel) {
  const { types: t } = babel;

  return {
    name: "refactor-regex-constr", // not required
    visitor: {
      CallExpression(path) {
        const callExpr = path.node;
        if (callExpr.arguments.length != 1) return;
        const argument = callExpr.arguments[0];
        if (!t.isStringLiteral(argument)) return;
        const calleeMemberExpr = callExpr.callee;
        if (!t.isMemberExpression(calleeMemberExpr)) return;
        if (!t.isRegExpLiteral(calleeMemberExpr.object)) return;
        let property = calleeMemberExpr.property;
        if (!t.isStringLiteral(property)) return;
        if (property.value != "constructor") return;
        
        path.replaceWith(
          t.regExpLiteral(argument.value.replace('/', '\\/'), '')
        );
      }
    }
  };
}