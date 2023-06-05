export default function (babel) {
  const { types: t } = babel;

  return {
    name: "undo-escape-call", // not required
    visitor: {
      CallExpression(path) {
        let callExpr = path.node;
        if (!t.isIdentifier(callExpr.callee)) return;
        if (callExpr.callee.name != "escape") return;
        if (callExpr.arguments.length != 1) return;
        if (!t.isStringLiteral(callExpr.arguments[0])) return;
        
        let newNode = t.stringLiteral(escape(callExpr.arguments[0].value));
        path.replaceWith(newNode);
      }
    }
  };
}
