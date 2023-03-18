export default function (babel) {
  const { types: t } = babel;

  return {
    name: "undo-function-escape-trick", // not required
    visitor: {
      MemberExpression(path) {
        let node = path.node;
        if (!t.isArrayExpression(node.object)) return;
        if (node.object.elements.length != 0) return;
        if (!t.isStringLiteral(node.property)) return;
        if (node.property.value === "flat") path.replaceWith(t.valueToNode(String(Array.prototype.flat)));
      },
      CallExpression(path) {
        let node = path.node;
        if (t.isCallExpression(node.callee) &&
            t.isCallExpression(node.callee.callee) &&
            t.isIdentifier(node.callee.callee.callee) &&
            node.callee.callee.callee.name === "Function" &&
            node.callee.callee.arguments.length === 1 &&
            t.isStringLiteral(node.callee.callee.arguments[0]) &&
            node.callee.callee.arguments[0].value === "return escape" &&
            t.isStringLiteral(node.arguments[0])
           ) {
            path.replaceWith(t.valueToNode(escape(node.arguments[0].value)));
        }
      }
    }
  };
}