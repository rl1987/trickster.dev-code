export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      "UnaryExpression|BinaryExpression"(path) {
        let result = path.evaluate();
        if (result.confident) {
          let valueNode = t.valueToNode(result.value);
          if (t.isLiteral(valueNode)) {
            path.replaceWith(valueNode);
          }
        }
      }
    }
  };
}
