export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      CallExpression(path) {
        let prop = path.node.callee.property;

        if (t.isStringLiteral(prop)) {
          path.node.callee.property = t.identifier(prop.value);
          path.node.callee.computed = false;
        }
      }
    }
  };
}