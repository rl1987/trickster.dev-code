export default function (babel) {
  const { types: t } = babel;

  return {
    name: "ast-transform", // not required
    visitor: {
      VariableDeclarator(path) {
        let node = path.node;
        if (!node.init) return;
        if (!t.isObjectExpression(node.init)) return;
        let binding = path.scope.getBinding(node.id.name);
        if (!binding.constant) return;
        let properties = node.init.properties;
        if (!properties) return;
        
        let kv = new Object();
                
        for (let prop of properties) {
          if (!t.isStringLiteral(prop.key)) return;
          let key = prop.key.value;
          if (!t.isFunctionExpression(prop.value) && !t.isStringLiteral(prop.value)) return;
          let value = prop.value;
          kv[key] = value;
        }
                                
        for (let refPath of binding.referencePaths) {
          if (!refPath.parentPath) return;
          let parentNode = refPath.parentPath.node;
          let key = parentNode.property.name;
          if (!key) key = parentNode.property.value;
          let value = kv[key];
		          
          if (t.isStringLiteral(value)) {
            refPath.parentPath.replaceWith(value); 
          } else if (t.isFunctionExpression(value)) {
            let fnName = key;
            // https://babeljs.io/docs/en/babel-types#functiondeclaration
            let functionDecl = t.functionDeclaration(
              t.identifier(key),
              value.params,
              value.body,
              value.generator,
              value.async
            );
            
            let parentOfDecl = path.parentPath.parentPath;
            parentOfDecl.unshiftContainer("body", functionDecl);
            refPath.parentPath.replaceWith(t.identifier(fnName)); 
          }
        }
        
        path.remove();
      } 
    }
  };
}