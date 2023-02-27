export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isStringLiteral(node.callee.object)) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value === "italics") {
           const fromStr = node.callee.object.value;
           if (node.arguments.length === 0) {
             path.replaceWith(t.valueToNode(fromStr.italics()));
           } 
        }
      }
    }
  };
}