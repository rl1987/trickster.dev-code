export default function (babel) {
  const { types: t } = babel;

  return {
    name: "undo-boolean-trick", // not required
    visitor: {
      Identifier(path) {
        let node = path.node;
       	if (!t.isBinaryExpression(path.parent)) return;
        if (path.parent.operator != "+") return;
        if (node.name === "Boolean") path.replaceWith(t.valueToNode(String(Boolean)));
      }
    }
  };
}
