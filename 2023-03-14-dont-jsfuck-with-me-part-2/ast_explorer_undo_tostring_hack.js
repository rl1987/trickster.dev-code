export default function (babel) {
  const { types: t } = babel;
  
  return {
    name: "undo-tostring-trick", // not required
    visitor: {
      MemberExpression(path) {
        let node = path.node;
        if (t.isIdentifier(node.object) && node.object.name === "String" &&
            t.isStringLiteral(node.property) && node.property.value === "name") {
          path.replaceWith(t.valueToNode("String"));
        } 
      },
      CallExpression(path) {
        let node = path.node;
        if (!t.isNumericLiteral(node.callee.object)) return;
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value != "toString") return;
        if (node.arguments.length != 1) return;
        let firstArg = node.arguments[0];
        if (!t.isNumericLiteral(firstArg)) return;
        
        path.replaceWith(
          t.valueToNode(node.callee.object.value.toString(firstArg.value))
        );
      }
    }
  };
}
