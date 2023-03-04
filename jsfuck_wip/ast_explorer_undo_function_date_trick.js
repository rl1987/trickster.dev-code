export default function (babel) {
  const { types: t } = babel;

  return {
    name: "undo-function-date-trick" // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        if (t.isCallExpression(node.callee) &&
            t.isCallExpression(node.callee.callee) &&
            t.isIdentifier(node.callee.callee.callee) &&
            node.callee.callee.callee.name === "Function" &&
            node.callee.callee.arguments.length === 1 &&
            t.isStringLiteral(node.callee.callee.arguments[0]) &&
            node.callee.callee.arguments[0].value === "return Date"
           ) {
            path.replaceWith(t.valueToNode(Date()));
        }
      }
    }
  };
}
