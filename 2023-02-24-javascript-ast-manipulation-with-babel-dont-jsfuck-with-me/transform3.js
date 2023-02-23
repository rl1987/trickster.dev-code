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
          } else {
            console.log("Irreducible", path.node, valueNode);
            path.replaceWith(valueNode);
            path.skip();
          }
        }
      },
      MemberExpression(path) {
      	let node = path.node;
      	if (!t.isStringLiteral(node.object)) return;
      	if (!t.isNumericLiteral(node.property)) return;
      	let character = node.object.value[node.property.value];
      	path.replaceWith(t.valueToNode(character));
      }
    }
  };
}