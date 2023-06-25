const babel = require("@babel/core");
const t = require("@babel/types");

const logASTChange = require("./debug.js").logASTChange;

module.exports = function (babel) {
  return {
    name: "eval-expr", // not required
    visitor: {
      "UnaryExpression|BinaryExpression"(path) {
        let node = path.node;
        
        if (t.isNumericLiteral(node.left) && t.isNumericLiteral(node.right)) {
          if (node.right.value === 0) {
           	if (node.left.value === 1) {
              let newNode = t.identifier('Infinity');
              logASTChange("eval-expr", node, newNode);
              path.replaceWith(newNode);
              return;
            } else if (node.left.value === 0) {
              let newNode = t.identifier('NaN');
              logASTChange("eval-expr", node, newNode);
              path.replaceWith(newNode);
              return;
            }
          }
        }

        let result = path.evaluate();
        if (result.confident) {
          let valueNode = t.valueToNode(result.value);
          if (t.isLiteral(valueNode)) {
            logASTChange("eval-expr", node, valueNode);
            path.replaceWith(valueNode);
          } else {
            logASTChange("eval-expr", node, valueNode);
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
          let valueNode = t.valueToNode(character);
          logASTChange("eval-expr", node, valueNode);
      	  path.replaceWith(valueNode);
        }
        
        if (t.isArrayExpression(node.object) &&
            node.object.elements.length == 0 &&
            t.isArrayExpression(node.property) &&
            node.property.elements.length == 0) {
          let valueNode = t.valueToNode(undefined);
          logASTChange("eval-expr", node, valueNode);
          path.replaceWith(valueNode);
        }
      }
    }
  };
}
