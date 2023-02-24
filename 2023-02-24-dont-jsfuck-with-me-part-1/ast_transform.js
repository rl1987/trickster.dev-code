export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      "UnaryExpression|BinaryExpression"(path) {
        let node = path.node;
        
        if (t.isNumericLiteral(node.left) && t.isNumericLiteral(node.right)) {
          if (node.right.value === 0) {
           	if (node.left.value === 1) {
              path.replaceWith(t.identifier('Infinity'));
              return;
            } else if (node.left.value === 0) {
              path.replaceWith(t.identifier('NaN'));
              return;
            }
          }
        }

        let result = path.evaluate();
        if (result.confident) {
          let valueNode = t.valueToNode(result.value);
          if (!t.isLiteral(valueNode)) {
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
      }
    }
  };
}
