export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      "UnaryExpression|BinaryExpression"(path) {
        let node = path.node;

        console.log(node);
        if (t.isArrayExpression(node.left) &&
            node.left.elements.length == 1 &&
            t.isBooleanLiteral(node.left.elements[0])
           ) {
          node.left = t.valueToNode(String(node.left.elements[0].value));
        }
        
        if (t.isStringLiteral(node.left) &&
            t.isMemberExpression(node.right) &&
            t.isArrayExpression(node.right.object) &&
            node.right.object.elements.length == 0 &&
            t.isArrayExpression(node.right.property) &&
            node.right.property.elements.length == 0) {
          node.right = t.valueToNode(String([][[]]));
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
        
        if (t.isArrayExpression(node.object) &&
            node.object.elements.length == 0 &&
            t.isStringLiteral(node.property)
            ) {
          path.replaceWith(t.valueToNode(String([][node.property.value])))
    	}
        
      	if (t.isStringLiteral(node.object) && t.isNumericLiteral(node.property)) {
      	  let character = node.object.value[node.property.value];
      	  path.replaceWith(t.valueToNode(character));
        }
      }
    }
  };
}
