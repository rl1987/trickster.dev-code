export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      UnaryExpression(path) {
        let result = path.evaluate();
        if (result.confident) {
          path.replaceWith(t.valueToNode(result.value));
        }
      }
    }
  };
}