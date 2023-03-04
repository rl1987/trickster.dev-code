export default function (babel) {
  const { types: t } = babel;

  return {
    name: "undo-string-constructor-trick", // not required
    visitor: {
      MemberExpression(path) {
        let node = path.node;
       	if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (!t.isStringLiteral(node.object)) return;
        if (node.object.value != "") return;
        if (!t.isStringLiteral(node.property)) return;
        if (node.property.value === "constructor") { 
          path.replaceWith(t.valueToNode(String(String)));
        }
      }
    }
  };
}