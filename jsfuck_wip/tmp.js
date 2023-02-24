export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      "BinaryExpression|UnaryExpression"(path) {
        let node = path.node;
        let evaluated = path.evaluate();
        if (!evaluated) return;
        if (!evaluated.confident) return;
        
        
        
        let value = evaluated.value;
        let valueNode = t.valueToNode(value);
        if (!t.isLiteral(valueNode)) return;
        
        path.replaceWith(valueNode);
      },
      MemberExpression(path) {
      	let node = path.node;
        if (t.isArrayExpression(node.object) &&
            node.object.elements.length == 0 &&
            t.isArrayExpression(node.property) &&
            node.property.elements.length == 0) {
          path.replaceWith(t.valueToNode(undefined));
        }
      }
    }
  };
}