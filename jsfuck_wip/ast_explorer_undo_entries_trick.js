export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isArrayExpression(node.callee.object)) return;
        if (node.callee.object.elements.length != 0) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value === "entries" && t.isBinaryExpression(path.parent)) {
          path.replaceWith(t.stringLiteral(String(Array.prototype.entries)));
        }
      }
    }
  };
}
