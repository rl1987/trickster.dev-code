export default function (babel) {
  const { types: t } = babel;

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
        
        path.replaceWith(t.stringLiteral(regexStr));
      }
    }
  };
}