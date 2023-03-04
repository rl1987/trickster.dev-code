export default function (babel) {
  const { types: t } = babel;
  
  return {
    name: "undo-concat-trick", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        
        if (!t.isMemberExpression(node.callee)) return;
        if (!t.isArrayExpression(node.callee.object)) return;
        if (node.callee.object.elements.length != 1) return;
        if (!t.isArrayExpression(node.callee.object.elements[0])) return;
        if (node.callee.object.elements[0].elements.length != 0) return;
        
        if (!t.isStringLiteral(node.callee.property)) return;
        if (node.callee.property.value != "concat") return;
        
        if (!t.isArrayExpression(node.arguments[0])) return;
        if (node.arguments[0].elements.length != 1) return;
        if (!t.isArrayExpression(node.arguments[0].elements[0])) return;
        if (node.arguments[0].elements[0].elements.length != 0) return;
        
        if (!t.isBinaryExpression(path.parent)) return;
        
        path.replaceWith(t.valueToNode(String([ [], [] ])));
      }
    }
  };
}
