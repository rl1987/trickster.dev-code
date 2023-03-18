export default function (babel) {
  const { types: t } = babel;

  return {
    name: "undo-slice-trick", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isStringLiteral(node.callee.object)) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.arguments.length != 1) return;
        if (node.callee.property.value === "slice" && 
            (t.isStringLiteral(node.arguments[0]) || 
             t.isNumericLiteral(node.arguments[0])) &&
             Number(node.arguments[0].value) === -1) {
          let fromStr = node.callee.object.value;
          path.replaceWith(t.valueToNode(fromStr.slice(-1)));
        }
      }
    }
  };
}
