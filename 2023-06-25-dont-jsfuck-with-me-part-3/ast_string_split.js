export default function (babel) {
  const { types: t } = babel;

  return {
    name: "string-split", // not required
    visitor: {
      CallExpression(path) {
        const callExpr = path.node;
        const memberExpr = callExpr.callee;
        if (!t.isMemberExpression(memberExpr)) return;
        let str = memberExpr.object;
        if (!t.isStringLiteral(str)) return;
        str = str.value;
        const fnName = memberExpr.property;
        if (!t.isStringLiteral(fnName)) return;
        if (fnName.value != "split") return;
        if (callExpr.arguments.length != 1) return;
        let separator = callExpr.arguments[0];
        if (!t.isStringLiteral(separator)) return;
        separator = separator.value;
        let components = str.split(separator);
        components = components.map(c => t.stringLiteral(c));
        
        path.replaceWith(t.arrayExpression(components));
      }
    }
  };
}