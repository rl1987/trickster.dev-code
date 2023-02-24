export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      CallExpression(path) {
        let node = path.node;
        let parent = path.parent;
        if (!t.isCallExpression(parent)) return;
        let callee = node.callee;
        if (!t.isMemberExpression(callee)) return;
        if (!t.isStringLiteral(callee.property)) return;
        let key1 = callee.property.value;
        if (!t.isMemberExpression(callee.object)) return;
        if (!t.isStringLiteral(callee.object.property)) return;
        let key2 = callee.object.property.value;
        if (key1 === "constructor" && (key2 === "filter" || key2 === "flat")) {
          let evalCallExpr = t.callExpression(t.identifier('eval'), 
                                                           node.arguments);
          path.parentPath.replaceWith(evalCallExpr);
        }
      },
      "UnaryExpression|BinaryExpression"(path) {
        let node = path.node;

        if (t.isArrayExpression(node.left) &&
            node.left.elements.length == 1 &&
            t.isBooleanLiteral(node.left.elements[0])
           ) {
          node.left = t.valueToNode(String(node.left.elements[0].value));
        }
        
        if (t.isArrayExpression(node.right) &&
            node.right.elements.length == 1 &&
            t.isBooleanLiteral(node.right.elements[0])
           ) {
          node.right = t.valueToNode(String(node.right.elements[0].value));
        }
        
        let result = path.evaluate();
        if (result.confident) {
          let valueNode = t.valueToNode(result.value);
          if (t.isLiteral(valueNode)) {
            path.replaceWith(valueNode);
          } else {
            path.replaceWith(valueNode);
            path.skip();
          }
        }
      },
      MemberExpression(path) {
      	let node = path.node;
        
        // https://stackoverflow.com/a/52986361/1044147
        function isNumeric(n) {
  	      return !isNaN(parseFloat(n)) && isFinite(n);
		}
          
        if (isNumeric(node.property.value)) {
          node.property = t.valueToNode(Number(node.property.value));
        }
        
      	if (t.isStringLiteral(node.object) && 
            t.isNumericLiteral(node.property)) {
      	  let character = node.object.value[node.property.value];
      	  path.replaceWith(t.valueToNode(character));
        }
        
        if (t.isArrayExpression(node.object) &&
            node.object.elements.length == 0 &&
            t.isArrayExpression(node.property) &&
            node.property.elements.length == 0) {
          path.replaceWith(t.valueToNode(undefined));
        }
        
        if (t.isArrayExpression(node.object) &&
            node.object.elements.length == 0 && 
            t.isStringLiteral(node.property) &&
            t.isBinaryExpression(path.parent) &&
            path.parent.operator === "+" &&
            node.property.value == "flat") {
          path.replaceWith(t.stringLiteral('function flat() { [native code] }'));
        }
      }
    }
  };
}
