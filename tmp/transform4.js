export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      FunctionDeclaration(path) {
        let node = path.node;
        if (node.id.name === "getEncodedStrings") {
          let encodedStringArrayExpr = node.body.body[0].declarations[0].init;
          let scope = path.scope;
          let binding = scope.getBinding(node.id.name);
          
          for (let refPath of binding.referencePaths) {
            if (refPath.parentPath.node.type === "CallExpression") {
              refPath.replaceWith(encodedStringArrayExpr);
            }
          }
          
          path.remove();
        }
      }        
    }
  };
}

