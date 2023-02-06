export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      BinaryExpression(path) {
        let evaluated = path.evaluate();
        if (!evaluated) return;
        
        let value = evaluated.value;
        let valueNode = t.valueToNode(value);
        if (!t.isLiteral(valueNode)) return;
        
        path.replaceWith(valueNode);
      }
    }
  };
}

